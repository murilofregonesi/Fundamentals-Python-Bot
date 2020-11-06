# -*- coding: utf-8 -*-
"""
Data Modeling

@input: Target Symbol (string)
        Modeling Data (DataFrame)
        GUI (Window)

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""
'''
# TODO
# only for testing, remove later
from FundamentusScraper import ScrapMarketData
from DataWrangling import WrangleModelingData
from GuiHandler import *
import pandas as pd
from PyQt5.QtWidgets import *
import sys

if QApplication.instance():
    app = QApplication.instance()
else:
    app = QApplication(sys.argv)

# Start Window
Gui = Window()

#app.setStyle('Fusion')
#app.exec_()
#sys.exit(app.exec_()) # Clean Exit

sym = 'BBAS3'
corrThreshold = 0.20 # Correlation Threshold
df_mkt = ScrapMarketData(sym, Gui) # Market DataFrame

if type(df_mkt) != pd.core.frame.DataFrame:
    Gui.AppendLog('* Market dataset is not valid. Analysis fineshed.')
else:
    df_model = WrangleModelingData(sym, df_mkt, corrThreshold, Gui) # Model DataFrame
# Call modeling now
'''
#%%

# TODO test
def PolynomialModeling(sym, df_model, Gui):

    #%% Polynomial Modeling
    
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn import linear_model
    from sklearn.model_selection import train_test_split
    
    # Set target symbol apart
    X_sym = df_model.loc[sym][df_model.columns != 'P/VP'] # Features
    y_sym = df_model.loc[sym][df_model.columns == 'P/VP'] # Target variable
    
    # Group modeling datasets
    X = df_model.iloc[:,df_model.columns != 'P/VP'].drop(sym, axis=0) # Features
    y = df_model.iloc[:,df_model.columns == 'P/VP'].drop(sym, axis=0) # Target variable
    
    # Remove price from features
    X_sym = X_sym.drop('Cotação')
    X = X.drop('Cotação', axis=1)
    
    # Split datasets
    test_size = 0.15
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        random_state=42)
    # Start Modeling
    import numpy as np
    
    maxDegree = 15
    scores = np.empty(maxDegree) # R2 Scores
    
    for polyDg in range(maxDegree):
        
        poly = PolynomialFeatures(degree = polyDg + 1) # Poly features
        X_train_tr = poly.fit_transform(X_train)
        
        poly_model = linear_model.LinearRegression() # Linear regression
        poly_model.fit(X_train_tr, y_train)
        
        X_test_tr = poly.fit_transform(X_test) # Score from test set
        y_test_pred = poly_model.predict(X_test_tr)
        
        scores[polyDg] = poly_model.score(X_test_tr, y_test) # Scores array
    
    # Select the best model degree
    import pandas as pd
    scores = pd.DataFrame(scores)
    scores['Distance'] = 1 - scores # Optimum result: R2 = 1, Distance = 0
    scores = scores.sort_values(by='Distance', ascending=True) # Sorting results
    
    polyDg = scores.index[0] + 1 # Best model
    Gui.AppendLog('Selected polynomial degree {}'.format(polyDg))
    
    # Recreate the best fit model
    poly = PolynomialFeatures(degree = polyDg)
    X_train_tr = poly.fit_transform(X_train)
    
    poly_model = linear_model.LinearRegression()
    poly_model.fit(X_train_tr, y_train)
    
    # Insert target symbol to the test set
    X_test = pd.concat([pd.DataFrame(X_sym).transpose(), X_test])
    y_test = pd.concat([pd.DataFrame(y_sym).transpose(), y_test])
    
    # Apply the model to the test set
    X_test_tr = poly.fit_transform(X_test)
    
    # P/VP Predictions for Test and Train sets
    y_test_pred = poly_model.predict(X_test_tr)
    y_train_pred = poly_model.predict(X_train_tr)
    
    
    #%% Market Price Predictions
    
    # Append Predictions to Target variable sets
    y_test['P/VP pred'] = y_test_pred
    y_train['P/VP pred'] = y_train_pred
    
    # Append Price to Target variable sets
    y_test['Cotação'] = df_model.loc[y_test.index,'Cotação']
    y_train['Cotação'] = df_model.loc[y_train.index,'Cotação']
    
    # Add Calculated VPA to Target variable sets
    y_test['VPA'] = y_test['Cotação'] / y_test['P/VP']
    y_train['VPA'] = y_train['Cotação'] / y_train['P/VP']
    
    # Add Calculated Expected Price
    y_test['Cotação pred'] = y_test['VPA'] * y_test['P/VP pred']
    y_train['Cotação pred'] = y_train['VPA'] * y_train['P/VP pred']
    
    # Predictions Standard Deviation
    stdDev_test = np.std(y_test['Cotação'] - y_test['Cotação pred'])
    stdDev_train = np.std(y_train['Cotação'] - y_train['Cotação pred'])
    
    Gui.AppendLog('\nTest Standard Deviation {dev:.2f}'.format(dev=stdDev_test))
    Gui.AppendLog('Train Standard Deviation {dev:.2f}'.format(dev=stdDev_train))
    
    
    #%% Show the Results
    
    import matplotlib.pyplot as plt
    from GuiHandler import PlotCanvas
    
    graph = PlotCanvas(Gui) # Start a Canvas
    
    # Price Data
    graph.ax.scatter(X_test.index, y_test['Cotação']) # Price
    graph.ax.scatter(X_test.index, y_test['Cotação pred']) # Price Predicted
    
    graph.ax.scatter(X_train.index, y_train['Cotação']) # Price
    graph.ax.scatter(X_train.index, y_train['Cotação pred']) # Price Predicted
    
    # Graph Config
    plt.ylabel('Price (R$)')
    plt.grid()
    plt.ylim(ymin=0)
    plt.legend(['Actual (test)', 'Prediction (test)',
                'Actual (train)', 'Prediction (train)'])
    plt.xticks(rotation=90)
    
    # Error Bars
    plt.errorbar(X_test.index, y_test['Cotação pred'], yerr = stdDev_test,
                 linestyle='None', ecolor='darkorange', capthick=3)
    plt.errorbar(X_train.index, y_train['Cotação pred'], yerr = stdDev_train,
                 linestyle='None', ecolor='r', capthick=3)
    
    plt.subplots_adjust(top = 0.99, bottom = 0.18, right = 0.99, left = 0.08,
                        hspace = 0, wspace = 0)
    graph.show()
