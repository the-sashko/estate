#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

if [[ ! -d data ]]
then
    mkdir data
    mkdir data/logs
    mkdir data/config

    chmod -R 755 data

    cp install/config/telegram.json data/config/telegram.json
    chmod 755 data/config/telegram.json
fi

cp install/config/telegram.json config/telegram.json
chmod 755 config/telegram.json

python3 -m venv "$(pwd)"

source bin/activate

pip3 install --upgrade pip
pip3 install -r requirements.txt

deactivate

cd "$currDir" || exit 1

exit 0

