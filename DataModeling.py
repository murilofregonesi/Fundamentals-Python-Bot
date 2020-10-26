# -*- coding: utf-8 -*-
"""
Data Modeling

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

from FundamentusScraper import ScrapMarketData
from DataWrangling import WrangleModelingData

sym = 'BBAS3' # Target Stock Symbol
corrThreshold = 0.25 # Correlation Threshold

df_mkt = ScrapMarketData(sym) # Market DataFrame
df_wrangle = df_mkt[:] # Market DataFrame Copy
df_model = WrangleModelingData(sym, df_wrangle, corrThreshold) # Model DataFrame

#%% Polynomial Modeling

from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn.model_selection import train_test_split

X = df_model.iloc[:,1:]
y = df_model.iloc[:,0]

# Split data for train and test
test_size = 0.1
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size = test_size,
                                                    random_state=42)
# Start Modeling
import numpy as np

maxDegree = 10
scores = np.empty(maxDegree) # R2 Scores

for polyDg in range(maxDegree):
    
    poly = PolynomialFeatures(degree = polyDg + 1)
    X_train_tr = poly.fit_transform(X_train)
    
    poly_model = linear_model.LinearRegression()
    poly_model.fit(X_train_tr, y_train)
    
    X_test_tr = poly.fit_transform(X_test)
    y_pred = poly_model.predict(X_test_tr)
    
    scores[polyDg] = poly_model.score(X_test_tr, y_test)

# Select the best model degree
import pandas as pd
scores = pd.DataFrame(scores)
scores['Distance'] = 1 - scores
scores = scores.sort_values(by='Distance',ascending=True)

polyDg = scores.index[0] + 1
print('Selected polynomial degree {}'.format(polyDg))

# Create the final model
poly = PolynomialFeatures(degree = polyDg)
X_train_tr = poly.fit_transform(X_train)

poly_model = linear_model.LinearRegression()
poly_model.fit(X_train_tr, y_train)

X_test_tr = poly.fit_transform(X_test)
y_pred = poly_model.predict(X_test_tr)

y_train_pred = poly_model.predict(X_train_tr)



# TODO
# Error Standard Deviation
stdDev = np.std(y_test - y_pred)
print('Error deviation {}'.format(stdDev))


# Plot the results
import matplotlib.pyplot as plt

figWidth = (X_test.index.shape[0] + X_train.index.shape[0]) * 0.28

fig = plt.figure(figsize = (figWidth,5))
ax1 = fig.add_subplot(111)
ax1.scatter(X_test.index, y_test)
ax1.scatter(X_test.index, y_pred)
ax1.scatter(X_train.index, y_train)
ax1.scatter(X_train.index, y_train_pred)
plt.ylabel('Cotação (R$)')
plt.grid()
plt.legend(['Real teste','Predição teste','Real treino','Predição treino'])
plt.xticks(rotation=90)
plt.errorbar(X_test.index, y_pred, yerr=stdDev, linestyle='None')
