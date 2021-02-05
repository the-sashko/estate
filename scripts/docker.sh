#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

cp "$scriptDir/cron.sh" cron.sh

rm -rf .git
rm -rf install
rm -rf scripts
rm -rf docs
rm -rf src
rm -rf config
rm -rf bin

rm -f .gitignore
rm -f LICENSE
rm -f README.md
rm -f requirements.txt

sudo docker build -t estate_parser .

rm -rf Dockerfile

sudo docker run -it --name estate_parser -v "$(pwd)/data":/storage/estate_parser/data estate_parser vi /storage/estate_parser/config/telegram.json

cd "$currDir" || exit 1

exit 0

