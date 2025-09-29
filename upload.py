#!/usr/bin/env python3
"""
upload.py

Upload all files from the local `data/` directory to s3://<bucket>/<data-prefix>/
and all files from `policies/` to s3://<bucket>/<policies-prefix>/

Usage examples:
  python upload.py --bucket fakebankdata
  python upload.py --bucket my-bucket --profile myawsprofile --dry-run

Notes:
- This script assumes AWS credentials are available via environment, shared credentials file or role.
- Do not embed credentials in scripts.
"""
import os
import sys
import argparse
import logging

try:
    import boto3
    from botocore.exceptions import ClientError
    from boto3.s3.transfer import TransferConfig
except Exception:
    print("boto3 is required. Install with: pip install boto3")
    sys.exit(1)


def iter_files(root_dir):
    """Yield full file paths under root_dir (skip directories)."""
    for dirpath, _, filenames in os.walk(root_dir):
        for name in filenames:
            yield os.path.join(dirpath, name)


def upload_file(s3_client, filename, bucket, key, config=None):
    try:
        s3_client.upload_file(filename, bucket, key, ExtraArgs={"ACL": "private"}, Config=config)
        logging.info("Uploaded %s -> s3://%s/%s", filename, bucket, key)
        return True
    except ClientError as e:
        logging.error("Failed to upload %s -> s3://%s/%s : %s", filename, bucket, key, e)
        return False


def upload_tree(s3_client, local_root, bucket, s3_prefix, config=None, dry_run=False):
    results = []
    if not os.path.isdir(local_root):
        logging.warning("Local folder %s does not exist, skipping", local_root)
        return results

    for path in iter_files(local_root):
        rel = os.path.relpath(path, local_root)
        key = s3_prefix.rstrip('/') + '/' + rel.replace(os.sep, '/')
        if dry_run:
            logging.info("[dry-run] would upload %s -> s3://%s/%s", path, bucket, key)
            results.append((path, key, 'dry-run'))
            continue
        ok = upload_file(s3_client, path, bucket, key, config=config)
        results.append((path, key, 'ok' if ok else 'failed'))
    return results


def summarize(results, name):
    total = len(results)
    ok = sum(1 for r in results if r[2] in ('ok', 'dry-run'))
    failed = sum(1 for r in results if r[2] == 'failed')
    logging.info("%s: total=%d ok/dry=%d failed=%d", name, total, ok, failed)


def main():
    parser = argparse.ArgumentParser(description="Upload data/ and policies/ to S3")
    parser.add_argument('--bucket', default='fakebankdata', help='S3 bucket name (default: fakebankdata)')
    parser.add_argument('--data-prefix', default='data', help='S3 prefix for data files (default: data)')
    parser.add_argument('--policies-prefix', default='policies', help='S3 prefix for policies files (default: policies)')
    parser.add_argument('--profile', help='AWS profile name to use from credentials file')
    parser.add_argument('--region', help='AWS region (optional)')
    parser.add_argument('--dry-run', action='store_true', help='Do not actually upload, just show actions')
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

    session_kwargs = {}
    if args.profile:
        session_kwargs['profile_name'] = args.profile

    session = boto3.session.Session(**session_kwargs)
    s3_client = session.client('s3', region_name=args.region) if args.region else session.client('s3')

    transfer_config = TransferConfig(multipart_threshold=8 * 1024 * 1024, max_concurrency=4)

    repo_root = os.path.abspath(os.path.dirname(__file__))
    data_root = os.path.join(repo_root, 'data')
    policies_root = os.path.join(repo_root, 'policies')

    logging.info("Starting upload to bucket=%s", args.bucket)
    logging.info("Data folder: %s -> s3://%s/%s/", data_root, args.bucket, args.data_prefix)
    logging.info("Policies folder: %s -> s3://%s/%s/", policies_root, args.bucket, args.policies_prefix)

    data_results = upload_tree(s3_client, data_root, args.bucket, args.data_prefix, config=transfer_config, dry_run=args.dry_run)
    policies_results = upload_tree(s3_client, policies_root, args.bucket, args.policies_prefix, config=transfer_config, dry_run=args.dry_run)

    summarize(data_results, 'data')
    summarize(policies_results, 'policies')

    if any(r[2] == 'failed' for r in (data_results + policies_results)):
        logging.error('One or more uploads failed')
        sys.exit(2)

    logging.info('Upload complete')


if __name__ == '__main__':
    main()
