"""
backtest_rpt.py

This script should report on results of a backtest.

This script should be called from ~/reg4us/script/backtest.bash

Demo:
~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_2001.csv
"""

import numpy  as np
import pandas as pd

# I should check cmd line args
import sys
if (len(sys.argv) != 2):
  print('You typed something wrong:')
  print('Demo:')
  print("~/anaconda3/bin/python ~/anaconda3/bin/python backtest_rpt.py ../public/csv/backtest_2001.csv")
  sys.exit()
  
csv_in = sys.argv[1]
bt_df  = pd.read_csv(csv_in)

# I should report long-only-effectiveness:
eff_lo_f = bt_df.pctlead.sum()

# I should report Linear-Regression-Effectiveness:
eff_sr = bt_df.pctlead * np.sign(bt_df.pred_linr)
bt_df['eff_linr'] = eff_sr
eff_linr_f        = eff_sr.sum()

# I should report Logistic-Regression-Effectiveness:
eff_sr = bt_df.pctlead * np.sign(bt_df.pred_logr - 0.5)
bt_df['eff_logr'] = eff_sr
eff_logr_f        = eff_sr.sum()

print('csv_in: '+csv_in)
print('Long-Only-Effectiveness: '          +str(eff_lo_f))
print('Linear-Regression-Effectiveness: '  +str(eff_linr_f))
print('Logistic-Regression-Effectiveness: '+str(eff_logr_f))

'bye'
