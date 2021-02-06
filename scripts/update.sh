#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.." || exit 1

git checkout -- .
git checkout -f master
git pull origin master

cd "$currDir" || exit 1

if [[ ! -f data/config/telegram.json ]]
then
    rm config/telegram.json
    cp data/config/telegram.json config/telegram.json
fi

exit 0
