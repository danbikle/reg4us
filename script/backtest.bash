#!/bin/bash

# ~/reg4us/script/backtest.bash

# This script should backtest Linear Regression and Logistic Regression with GSPC prices.

# If you have questions, e-me: bikle101@gmail.com

# I should cd to the right place:
cd ~/reg4us/script/

# I should create a folder to hold CSV data:
mkdir -p ~/reg4us/public/csv/

# I should get prices:
# curl 'https://tkrprice.herokuapp.com/static/gspc.csv' > ~/reg4us/public/csv/gspc2.csv
# Better way:
./curlprices.bash

# I should compute features from the prices:
~/anaconda3/bin/python genf.py SLOPES='[2,3,4,5,6,7,8,9]'

rm -f /tmp/learn_tst_rpt.py.reg42.txt
rm -f ../public/csv/backtest_*csv
rm -f ../public/backtest_$yr.png
thisyr=`date +%Y`
for (( yr=2000; yr<=${thisyr}; yr++ ))
do
    echo Busy...
    echo backtesting: $yr                                             >> /tmp/learn_tst_rpt.py.reg42.txt
    ~/anaconda3/bin/python learn_tst_rpt.py TRAINSIZE=25 TESTYEAR=$yr >> /tmp/learn_tst_rpt.py.reg42.txt 2>&1
    mv ../public/csv/reg4.csv ../public/csv/backtest_$yr.csv
    mv ../public/rgb.png ../public/backtest_$yr.png
    ~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_${yr}.csv > /tmp/backtest_rpt_${yr}.py.reg42.txt 2>&1
done

# I should aggregate backtest results and then report:
cat ../public/csv/backtest_*.csv | sed -n 1p           > /tmp/backtest_all.reg42.csv
cat ../public/csv/backtest_*.csv | sort|grep -v cdate >> /tmp/backtest_all.reg42.csv
cp /tmp/backtest_all.reg42.csv ../public/csv/backtest_all.csv
~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_all.csv
~/anaconda3/bin/python backtest_rgb.py ../public/csv/backtest_all.csv

# backtest.bash clobbers data created by night.bash
# I should fix that:
./night.bash

exit
