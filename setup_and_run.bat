@echo off
echo Setting up the Document Summarization App...

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install required libraries
pip install spacy networkx scikit-learn docx2txt PyPDF2 pyinstaller

REM Download spaCy language models
python -m spacy download ja_core_news_sm
python -m spacy download en_core_web_sm

REM Get spaCy installation path
for /f "tokens=*" %%i in ('python -c "import spacy; print(spacy.__path__[0])"') do set SPACY_PATH=%%i

REM Create executable
pyinstaller --onefile --windowed --add-data "%SPACY_PATH%\lang\ja;spacy\lang\ja" --add-data "%SPACY_PATH%\lang\en;spacy\lang\en" --hidden-import="spacy" --hidden-import="spacy.lang.ja" --hidden-import="spacy.lang.en" SummaryApp.py

echo.
echo Setup complete! The executable has been created in the 'dist' folder.
echo.

REM Run the executable
start "" "dist\SummaryApp.exe"

pause
