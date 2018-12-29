"""
whatif_rpt.py

This script should be called by whatif.bash

# This script helps me understand some whatif-scenarios.

This script should generate some static content each night
after the market has closed and the most recent GSPC-closing-price
is available from Yahoo.

If you have questions, e-me: bikle101@gmail.com
Demo:
~/anaconda3/bin/python whatif_rpt.py
"""

import pandas as pd

rpt_df = pd.read_csv('../public/csv/whatif_pred.csv')
rpt_df.to_html('../app/views/pages/_whatif_pred.erb', index=False)

# I should plot 'Logistic Regression Prediction' vs Whatif_Price

pvprice_df = rpt_df.set_index(['Whatif_Price'])

import matplotlib
matplotlib.use('Agg')
# Order is important here.
# Do not move the next import:
import matplotlib.pyplot as plt

pvprice_df[['Logistic Regression Prediction']].plot.line(title="Prediction vs Price", figsize=(11,7))
# I should plot
plt.grid(True)
plt.savefig('../public/logr_price.png')
plt.close()

pvprice_df[['Linear Regression Prediction']].plot.line(title="Prediction vs Price", figsize=(11,7))
# I should plot
plt.grid(True)
plt.savefig('../public/linr_price.png')
plt.close()

'bye'
