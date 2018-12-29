"""
whatif.py

This script should apply pctchange to last price.

Demo:
python whatif.py -0.4
"""

import datetime
import pandas as pd
import pdb

# I should check cmd line arg
import sys
if (len(sys.argv) != 2):
  print('You typed something wrong:')
  print('Demo:')
  print('~/anaconda3/bin/python whatif.py -0.4')
  sys.exit()
pctchange_f = float(sys.argv[1]) / 100.0
whatif_df   = pd.read_csv('../public/csv/whatif.csv')
lastp_f     = float(whatif_df.iloc[-1:].cp)
# I should calculate the new price:
newcp_f   = lastp_f * pctchange_f + lastp_f
idxlast_i = whatif_df.iloc[-1:].index[0]
whatif_df.loc[idxlast_i,'cp'] = newcp_f

# I should increment the date of the last price

# I should get the latest cdate:
maxdate_s = whatif_df.cdate.iloc[idxlast_i]

# I should convert it to a datetime:
maxdate_d = datetime.datetime.strptime(maxdate_s, '%Y-%m-%d')

# I should convert the datetime to a string telling me day-name:
maxday_s = datetime.datetime.strftime(maxdate_d, '%a')

# If maxday_s is Fri I should calc the date 3 days after maxdate_d
if maxday_s == 'Fri':
    whatifdate_d = maxdate_d + datetime.timedelta(days=3)
else:
    whatifdate_d = maxdate_d + datetime.timedelta(days=1)

# I should convert whatifdate_d to string:
whatifdate_s = datetime.datetime.strftime(whatifdate_d, '%Y-%m-%d')

# I should update the DF:
whatif_df.loc[idxlast_i,'cdate'] = whatifdate_s

# I should save my work:
whatif_df.to_csv('../public/csv/gspc2.csv', float_format='%4.4f', index=False)

'bye'

