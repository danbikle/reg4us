#!/bin/bash

# ~/reg4us/script/whatif.bash

# This script helps me understand some whatif-scenarios.

# This script should generate some static content each night
# after the market has closed and the most recent GSPC-closing-price
# is available from Yahoo.

# If you have questions, e-me: bikle101@gmail.com

# I should cd to the right place:
cd ~/reg4us/script/

# I should create a folder to hold CSV data:
mkdir -p ~/reg4us/public/csv/

# I should prep CSV:
echo 'Whatif_Price,Linear Regression Prediction,Logistic Regression Prediction' > ../public/csv/whatif_pred.csv

# I should get prices:
./curlprices.bash

cp ~/reg4us/public/csv/gspc2.csv  ~/reg4us/public/csv/gspc2.csv.bak
for pctchange in -1.0 -0.8 -0.6 -0.4 -0.2 0.0 0.2 0.4 0.6 0.8 1.0
do
    echo $pctchange
    cp ~/reg4us/public/csv/gspc2.csv         ~/reg4us/public/csv/whatif.csv
    tail -1 ~/reg4us/public/csv/gspc2.csv >> ~/reg4us/public/csv/whatif.csv
    # I should apply pctchange to last price:
    ~/anaconda3/bin/python whatif.py $pctchange

    # I should compute features from the prices:
    ~/anaconda3/bin/python genf.py SLOPES='[2,3,4,5,6,7,8,9]'

    # I should learn, test, and report:
    tstyr=`date +"%Y"`
    echo $tstyr
    ~/anaconda3/bin/python learn_tst_rpt.py TRAINSIZE=25 TESTYEAR=$tstyr > /tmp/learn_tst_rpt.py.reg42.out 2>&1

    tail -1 ../public/csv/reg4.csv | awk -F, '{print $2"," $(NF-1)"," $NF}' >> ../public/csv/whatif_pred.csv
    cp ~/reg4us/public/csv/gspc2.csv.bak ~/reg4us/public/csv/gspc2.csv
done

# I should see predictions for ascending price points:
cat ../public/csv/whatif_pred.csv

~/anaconda3/bin/python whatif_rpt.py

# I should note the current price:
tail -1 ~/reg4us/public/csv/gspc2.csv > ../app/views/pages/_current_price.erb

exit
