#!/bin/bash

currDir=$(pwd)
scriptDir="$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd)"

cd "$scriptDir/.."

git checkout -- .
git checkout -f master
git pull origin master

cd "$currDir"

exit
