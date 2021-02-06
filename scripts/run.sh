#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

./scripts/update.sh

source bin/activate

python3 src/run.py

deactivate

cd "$currDir" || exit 1

exit 1
