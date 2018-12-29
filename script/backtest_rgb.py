"""
~/reg4us/script/backtest_rgb.py

This script should plot an RGB visualization of predictions.

This script should be called from ~/reg4us/script/backtest.bash

Demo:
~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_all.csv
"""

import numpy  as np
import pandas as pd

# I should check cmd line args
import sys
if (len(sys.argv) != 2):
  print('You typed something wrong:')
  print('Demo:')
  print("~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_all.csv")
  sys.exit()

csv_in = sys.argv[1]
bt_df  = pd.read_csv(csv_in)

rgb0_df          = bt_df.iloc[:-1][['cdate','cp']] # I should avoid the last row.
rgb0_df['cdate'] = pd.to_datetime(rgb0_df['cdate'], format='%Y-%m-%d')
rgb0_df.columns  = ['cdate','Long Only']
# I should create effectiveness-line for Linear Regression predictions.
# I have two simple rules:
# 1. If blue line moves 1%, then model-line moves 1%.
# 2. If model is True, model-line goes up.

blue_l      = bt_df.cp.tolist()
pred_linr_l = bt_df.pred_linr.tolist()
# linr_l should collect values to be plotted:
linr_l = [blue_l[0]] # I should initialize linr line
len_i  = rgb0_df.index.size
for row_i in range(len_i):
  blue_delt = blue_l[row_i+1]-blue_l[row_i]
  linr_delt = np.sign(pred_linr_l[row_i]) * blue_delt
  # I should collect 1 value:
  linr_l.append(linr_l[row_i]+linr_delt)
# I should copy the collected values into a DF:
rgb0_df['Linear Regression'] = linr_l[:-1] # avoid last value

# I should create effectiveness-line for Logistic Regression predictions.
pred_logr_l = bt_df.pred_logr.tolist()
# logr_l should collect values to be plotted:
logr_l = [blue_l[0]] # I should initialize logr line
for row_i in range(len_i):
  blue_delt = blue_l[row_i+1]-blue_l[row_i]
  logr_delt = np.sign(pred_logr_l[row_i]-0.5) * blue_delt
  # I should collect 1 value:
  logr_l.append(logr_l[row_i]+logr_delt)
rgb0_df['Logistic Regression'] = logr_l[:-1] # avoid last value

# I should have the data I want.
# I should plot 3 lines with cdate as x-axis:
# Effectiveness of: Long-Only, Linear Regression, Logistic Regression
import matplotlib
matplotlib.use('Agg')
# Order is important here.
# Do not move the next import:
import matplotlib.pyplot as plt

rgb1_df = rgb0_df.set_index(['cdate']) # make cdate the x-axis
# plot the remaining 3 columns:
rgb1_df.plot.line(title="RGB Effectiveness Visualization", figsize=(11,7))
plt.savefig('../public/backtest_rgb.png')
plt.close()
'bye'
