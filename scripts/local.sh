#!/usr/bin/bash

PROFILE=default # Default aws prfoile in ~/.aws/config

export AWS_PROFILE=${PROFILE}

echo "Building application from build.sh..."
bash ./scripts/build.sh
clear
sam local start-api -t templates/template.yml --env-vars templates/variables.json
