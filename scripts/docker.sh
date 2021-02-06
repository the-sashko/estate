#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

cp "$scriptDir/cron.sh" cron.sh

sudo docker build -t estate_parser .

sudo docker run -d --name estate_parser -v "$(pwd)/data":/storage/estate_parser/data estate_parser            

rm -rf data

./scripts/install.sh

rm -rf .git
rm -rf install
rm -rf scripts
rm -rf docs
rm -rf src
rm -rf config
rm -rf bin
rm -rf include
rm -rf lib
rm -rf lib64

rm -f .gitignore
rm -f LICENSE
rm -f README.md
rm -f requirements.txt
rm -f Dockerfile
rm -f pip-selfcheck.json
rm -f pyvenv.cfg

cd "$currDir" || exit 1

exit 0

