@echo off
echo Installing dependencies for the Document Summarization App...

REM Upgrade pip
python -m ensurepip --upgrade
python -m pip install --upgrade pip

REM Install required libraries
python -m pip install spacy networkx scikit-learn docx2txt PyPDF2 pyinstaller

REM Download spaCy language models
python -m spacy download ja_core_news_sm
python -m spacy download en_core_web_sm

echo.
echo Installation complete!
echo If you encountered any errors, please check the error messages and try to resolve them manually.
echo.
pause
