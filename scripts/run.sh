#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

./scripts/update.sh

cd "$scriptDir/.." || exit 1

source .env/bin/activate

./src/run.py

deactivate

cd "$currDir" || exit 1

exit 1
