# Installation Guide

## Install With Docker

`git clone https://github.com/the-sashko/estate.git <YOUR_PROJECT>`

`cd <YOUR_PROJECT>`

`/bin/bash scripts/docker.sh`

`Edit data/config/telegram.json`

Add To Crontab

`* * * * * /bin/bash <PATH_TO_YOUR_PROJECT>/cron.sh`

## Install Without Docker

**Strongly recommend use this way only for development or debugging**

`git clone https://github.com/the-sashko/estate.git <YOUR_PROJECT>`

`cd <YOUR_PROJECT>`

`/bin/bash scripts/install.sh`

Edit `data/config/telegram.json`

Run parser `/bin/bash scripts/run.sh`
