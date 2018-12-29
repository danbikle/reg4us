#!/bin/bash

# ~/reg4us/script/night_pull_push.bash

# This script should git pull, run night.bash, git commit, git push

# I should dot the .bashrc in case this script called from cron:
.  ~/.bashrc
cd ~/reg4us/
git pull heroku master

cd script/
./night.bash

cd ~/reg4us/
git commit -am night_pull_push.bash.done
git push heroku master

exit
