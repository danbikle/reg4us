#!/bin/bash

# railss.bash

# This script should start a webserver for development efforts.

cd ${HOME}/reg4us/ # assuming I put the repo in ${HOME}/reg4/

# I should start a rails server on all interfaces on port 4742:
bin/rails server -b 0.0.0.0 -p 4742

exit
