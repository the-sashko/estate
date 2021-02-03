#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.."

cp "$scriptDir/cron.sh" cron.sh

rm -rf .git
rm -rf data
rm -rf install
rm -rf scripts
rm -rf docs
rm -rf src

rm -f .gitignore
rm -f LICENSE
rm -f README.md
rm -f requirements.txt

cd docker

sudo docker build -t estate_parser .

cd ..

mkdir data

sudo docker run -d -p 80:80 --name estate_parser -v "$(pwd)/data":/storage/estate_parser/data estate_parser

cd "$currDir"

exit
