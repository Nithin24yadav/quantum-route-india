@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
python -m pip install streamlit
python -m streamlit run app.py
pause
