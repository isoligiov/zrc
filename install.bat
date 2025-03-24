@echo off
python -m venv env
call env\Scripts\activate
pip install -r requirements.txt

set /p appName=APP_NAME: 
set outputFile=.env
(
  echo APP_NAME=%appName%
) > %outputFile%

echo .env initialized