#!/bin/bash

# curlprices.bash

# I should create a folder to hold CSV data:
mkdir -p ~/reg4us/public/csv/

# This script should filter prices from tkrprice.herokuapp.com
echo cdate,cp > ~/reg4us/public/csv/gspc2.csv
/usr/bin/curl https://tkrprice.herokuapp.com/static/gspc.csv|\
    grep 0      |\
    grep -v null|\
    awk -F, '{print $1","$5}' >> ~/reg4us/public/csv/gspc2.csv
exit
