#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

mkdir logs
chmod -R 775 logs

cp install/config/credentials.json config/credentials.json
chmod 775 config/credentials.json

cd "$currDir" || exit 1

exit 1
