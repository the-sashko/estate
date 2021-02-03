#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

mkdir logs
chmod -R 755 logs

cp install/config/credentials.json config/credentials.json
chmod 755 config/credentials.json

python3 -m venv .env

source .env/bin/activate

pip3 install -r requirements.txt

deactivate

cd "$currDir" || exit 1

exit 1
