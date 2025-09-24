# Customer Data Model

## Overview
This data model defines the customer table, which is referenced by other risk domain tables to ensure referential integrity and consistency.

## Table: customers
- **customer_id** (PK): Unique identifier
- **name**: Customer name
- **date_of_birth**: Date of birth
- **address**: Address
- **customer_since**: Date customer joined
- **segment**: Retail/Corporate/SME

## Data Population Guidelines
- Use Faker to generate realistic names, addresses, and dates of birth.
- Ensure customer_id is unique and referenced by other domain tables.
- Segment distribution should reflect a plausible mix of retail, corporate, and SME customers.

---

## Table: customer_interactions
- **interaction_id** (PK): Unique identifier
- **customer_id** (FK): References customers.customer_id
- **interaction_date**: Date and time of interaction
- **interaction_type**: Phone call, email, branch visit, chat, etc.
- **agent_id**: Identifier for staff member (optional)
- **interaction_text**: Unstructured text (e.g., call transcript, email body, chat log)

## Data Population Guidelines for Interactions
- Generate multiple interactions per customer over time, with plausible distribution of types.
- Use Faker and synthetic text generation for interaction_text (e.g., sample call transcripts, email bodies).
- Ensure referential integrity: all interactions reference valid customers.
- Vary interaction content to reflect typical banking scenarios (account queries, complaints, loan discussions, etc.).

---

## Allowed Values for Dimensional Columns

### Segment
- Allowed values: [Retail, Corporate, SME]

### Interaction Type
- Allowed values: [Phone Call, Email, Branch Visit, Chat, Mobile App]

### Agent ID
- Allowed values: Alphanumeric staff identifiers (e.g., AGT001, AGT002)

### Geography (Address)
- Use valid Australian address formats and postcodes

---

## Australian Context
- Customer data should reflect Australian demographics and address formats.
- Use Australian names, addresses, and segments (e.g., retail, SME, corporate).
- All monetary values in AUD.
- Compliance with Australian privacy and data protection standards (Privacy Act 1988).
