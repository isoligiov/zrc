#!/bin/zsh

cd "$(dirname "$0")";

python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

read "appName?APP_NAME: "
outputFile=".env"
(
  echo "APP_NAME=$appName"
) > $outputFile

echo ".env initialized"