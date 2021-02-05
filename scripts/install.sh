#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

mkdir data
mkdir data/logs

chmod -R 755 data

cp install/config/telegram.json config/telegram.json
chmod 755 config/telegram.json

ln -s config data/config

python3 -m venv .env

source .env/bin/activate

pip3 install --upgrade pip

pip3 install -r requirements.txt

deactivate

cd "$currDir" || exit 1

exit 0
