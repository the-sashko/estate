#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

cp "$scriptDir/cron.sh" cron.sh

cp install/config/telegram.json data/config/telegram.json

vi data/config/telegram.json

rm -rf .git
rm -rf install
rm -rf scripts
rm -rf docs
rm -rf src

rm -f .gitignore
rm -f LICENSE
rm -f README.md
rm -f requirements.txt

cd docker || exit 1

sudo docker build -t estate_parser .

cd .. || exit 1

mkdir data

sudo docker run -d -p 80:80 --name estate_parser -v "$(pwd)/data":/storage/estate_parser/data estate_parser

cd "$currDir" || exit 1

exit
