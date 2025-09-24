@echo off
REM Create virtual environment and install requirements
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
@echo Environment setup complete.
