"""
learn_tst_rpt.py

This script should learn from observations in ~/reg4us/public/csv/feat.csv

Then it should test its learned models on observations later than the training observations.

Next it should report effectiveness of the models.

Demo:
~/anaconda3/bin/python learn_tst_rpt.py TRAINSIZE=25 TESTYEAR=2000

Above demo should train from 25 years of observations and predict each day of 2000
"""

import numpy  as np
import pandas as pd

# I should check cmd line args
import sys
if (len(sys.argv) != 3):
  print('You typed something wrong:')
  print('Demo:')
  print("~/anaconda3/bin/python learn_tst_rpt.py TRAINSIZE=30 TESTYEAR=2015")
  sys.exit()

# I should get cmd line args:
trainsize     = int(sys.argv[1].split('=')[1])
testyear_s    =     sys.argv[2].split('=')[1]
train_end_i   = int(testyear_s)
train_end_s   =     testyear_s
train_start_i = train_end_i - trainsize
train_start_s = str(train_start_i)
# train and test observations should not overlap:
test_start_i  = train_end_i
test_start_s  = str(test_start_i)
test_end_i    = test_start_i+1
test_end_s    = str(test_end_i)

feat_df  = pd.read_csv('../public/csv/feat.csv')
train_sr = (feat_df.cdate > train_start_s) & (feat_df.cdate < train_end_s)
test_sr  = (feat_df.cdate > test_start_s)  & (feat_df.cdate < test_end_s)
# I should not hard-code column names.
# feat_l   = ['slope2', 'slope3', 'slope4', 'slope5', 'slope6', 'slope7', 'slope8', 'slope9', 'dow', 'moy']
# I should read column names from feat.csv
# I should assume the features start at 3rd column.
feat_l   = feat_df.columns.tolist()[3:]
train_df = feat_df[feat_l].loc[train_sr]
test_df  = feat_df[feat_l].loc[test_sr]

# I should build a Linear Regression model from feature columns in train_df:
x_train_a = np.array(train_df)
y_train_a = np.array(feat_df.pctlead.loc[train_sr])
from sklearn import linear_model
linr_model = linear_model.LinearRegression()
# I should learn:
linr_model.fit(x_train_a, y_train_a)
# Now that I have learned, I should predict:
x_test_a       = np.array(test_df)
predictions_a  = linr_model.predict(x_test_a)
# predictions_df = test_df.copy()
predictions_df = feat_df[['cdate', 'cp', 'pctlead']].loc[test_sr]
predictions_df['pred_linr'] = predictions_a.reshape(predictions_a.shape[0],1)

# I should build a Logistic Regression model.
logr_model = linear_model.LogisticRegression()
# I should get classification from y_train_a:
# Should I prefer median over mean?:
# class_train_a = (y_train_a > np.median(y_train_a))
class_train_a = (y_train_a > np.mean(y_train_a))
# I should learn:
logr_model.fit(x_train_a, class_train_a)
# Now that I have learned, I should predict:
predictions_a               = logr_model.predict_proba(x_test_a)
predictions_df['pred_logr'] = predictions_a[:,1]

# I should create a CSV to report from:
predictions_df.to_csv('../public/csv/reg4.csv', float_format='%4.6f', index=False)

# I should report long-only-effectiveness:
eff_lo_f = predictions_df.pctlead.sum()
print('Long-Only-Effectiveness:')
print(eff_lo_f)

# I should report Linear-Regression-Effectiveness:
eff_sr = predictions_df.pctlead * np.sign(predictions_df.pred_linr)
predictions_df['eff_linr'] = eff_sr
eff_linr_f                 = np.sum(eff_sr)
print('Linear-Regression-Effectiveness:')
print(eff_linr_f)

# I should report Logistic-Regression-Effectiveness:
eff_sr = predictions_df.pctlead * np.sign(predictions_df.pred_logr - 0.5)
predictions_df['eff_logr'] = eff_sr
eff_logr_f                 = eff_sr.sum()
print('Logistic-Regression-Effectiveness:')
print(eff_logr_f)

# I should use html to report:
model_l = ['Long Only', 'Linear Regression', 'Logistic Regression']
eff_l   = [eff_lo_f, eff_linr_f, eff_logr_f]

rpt_df                  = pd.DataFrame(model_l)
rpt_df.columns          = ['model']
rpt_df['effectiveness'] = eff_l
rpt_df.to_html(        '../app/views/pages/_agg_effectiveness.erb',      index=False)
predictions_df.to_html('../app/views/pages/_detailed_effectiveness.erb', index=False)

# I should plot Pct Lead Observations vs Linear Regression Predictions
linr1_df = predictions_df[['pred_linr','pctlead']].iloc[:-1]

# I should plot Pct Lead Observations vs Logistic Regression Predictions
logr1_df = predictions_df[['pred_logr','pctlead']].iloc[:-1]

import matplotlib
matplotlib.use('Agg')
# Order is important here.
# Do not move the next import:
import matplotlib.pyplot as plt

fig = plt.figure()
fig.suptitle('Scatter Plot Of Pct Lead Observations vs Linear Regression Predictions')
plt.scatter(linr1_df.pred_linr,linr1_df.pctlead)
plt.savefig('../public/linr1.png')
plt.close()

fig = plt.figure()
fig.suptitle('Scatter Plot Of Pct Lead Observations vs Logistic Regression Predictions')
plt.scatter(logr1_df.pred_logr,logr1_df.pctlead)
plt.savefig('../public/logr1.png')
plt.close()

fig = plt.figure()
fig.suptitle('Logistic Regression Predictions vs Linear Regression Predictions')
plt.scatter(predictions_df.pred_linr, predictions_df.pred_logr)
plt.savefig('../public/linlog.png')
plt.close()

rgb0_df          = predictions_df.iloc[:-1][['cdate','cp']]
rgb0_df['cdate'] = pd.to_datetime(rgb0_df['cdate'], format='%Y-%m-%d')
rgb0_df.columns  = ['cdate','Long Only']
# I should create effectiveness-line for Linear Regression predictions.
# I have two simple rules:
# 1. If blue line moves 1%, then model-line moves 1%.
# 2. If model is True, model-line goes up.
len_i       = len(rgb0_df)
blue_l      = [cp       for cp       in predictions_df.cp]
pred_linr_l = [pred_linr for pred_linr in predictions_df.pred_linr]
linr_l      = [blue_l[0]]
for row_i in range(len_i):
  blue_delt = blue_l[row_i+1]-blue_l[row_i]
  linr_delt = np.sign(pred_linr_l[row_i]) * blue_delt
  linr_l.append(linr_l[row_i]+linr_delt)
rgb0_df['Linear Regression'] = linr_l[:-1]

# I should create effectiveness-line for Logistic Regression predictions.
pred_logr_l = [pred_logr for pred_logr in predictions_df.pred_logr]
logr_l      = [blue_l[0]]
for row_i in range(len_i):
  blue_delt = blue_l[row_i+1]-blue_l[row_i]
  logr_delt = np.sign(pred_logr_l[row_i]-0.5) * blue_delt
  logr_l.append(logr_l[row_i]+logr_delt)
rgb0_df['Logistic Regression'] = logr_l[:-1]

rgb1_df = rgb0_df.set_index(['cdate'])
rgb1_df.plot.line(title="RGB Effectiveness Visualization "+testyear_s, figsize=(11,7))
plt.savefig('../public/rgb.png')
plt.close()

'bye'
