@echo off
echo Activating virtual environment...
call venv\Scripts\activate

echo Running Streamlit App...
streamlit run app.py

pause
