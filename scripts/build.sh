#!/usr/bin/bash

echo "Building application..."

rm requirements.txt
pipenv lock -r > requirements.txt
pipenv run pip install -r requirements.txt -t src/build/ --upgrade
command cp -rf src/*.py src/build/
