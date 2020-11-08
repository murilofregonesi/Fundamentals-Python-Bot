# -*- coding: utf-8 -*-
"""
Data Modeling

@input: Target Symbol (string)
        Modeling Data (DataFrame)
        GUI (Window)

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

def PolynomialModeling(sym, df_model, Gui):

    #%% Split Train and Test Data Sets
    
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
    test_size = 0.25
    Gui.AppendLog('\nSize of Test set: {}%'.format(test_size*100))
    
    X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                        test_size=test_size,
                                                        random_state=42)
    
    
    #%% Perform Ridge Regression
    
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import GridSearchCV
    
    
    maxDegree = 12 # Maximum Polynomial degree
    nFolds = 4     # Cross-Validation folds
    alphaNum = 30  # Number of alpha values
    
    import numpy as np
    scores = np.empty(maxDegree) # CV Scores
    alphas = np.empty(maxDegree) # Alphas
    
    for polyDg in range(maxDegree):
    
        # Create Polynomial Sets
        poly = PolynomialFeatures(degree = polyDg + 1)
        X_train_tr = poly.fit_transform(X_train)
        
        # Implement Grid Search
        ridge = Ridge(normalize=True)
        alphaValues = np.geomspace(1e-3, 10, num=alphaNum)
        gridParams = [{'alpha':alphaValues}]
        grid = GridSearchCV(ridge, gridParams, cv=nFolds)
        
        # Mean cross-validated score of the best_estimator
        grid.fit(X_train_tr, y_train)
        scores[polyDg] = grid.best_score_
        alphas[polyDg] = grid.best_params_['alpha']
        
    
    # Select the best Polynomial model
    import pandas as pd
    scores = pd.DataFrame(scores)
    
    scores['Distance'] = 1 - scores # Optimum result: R2 = 1, Distance = 0
    scores = scores.sort_values(by='Distance', ascending=True) # Sorting results
    
    polyDg = scores.index[0] + 1 # Best model degree
    Gui.AppendLog('\nSelected polynomial degree {}'.format(polyDg))
    
    alpha = alphas[scores.index[0]]
    Gui.AppendLog('Selected Ridge Alpha {}'.format(alpha))
    
    
    # Recreate the best fit model
    del poly
    del X_train_tr
    del ridge
    
    poly = PolynomialFeatures(degree = polyDg) # Create Polynomial Sets
    X_train_tr = poly.fit_transform(X_train)
    
    ridge = Ridge(alpha=alpha, normalize=True) # Implement Ridge Regression
    ridge.fit(X_train_tr, y_train)
    
    
    #%% Market Price Predictions
    
    # Insert target Symbol to the test set
    # Place @1st
    X_test = pd.concat([pd.DataFrame(X_sym).transpose(), X_test])
    y_test = pd.concat([pd.DataFrame(y_sym).transpose(), y_test])
    
    # P/VP Predictions for Test and Train sets
    y_train_pred = ridge.predict(X_train_tr)
    
    X_test_tr = poly.fit_transform(X_test)
    y_test_pred = ridge.predict(X_test_tr)
    
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
    
    Gui.AppendLog('\nTest Standard Deviation R$ {dev:.2f}'.format(dev=stdDev_test))
    Gui.AppendLog('Train Standard Deviation R$ {dev:.2f}'.format(dev=stdDev_train))
    
    Gui.AppendLog('\n* {}'.format(sym))
    Gui.AppendLog('Actual price:\tR$ {p:.2f}'.format(p=y_test.loc[sym,'Cotação']))
    Gui.AppendLog('Price prediction:\tR$ {p:.2f}'.format(p=y_test.loc[sym,'Cotação pred']))
    Gui.AppendLog('Dev prediction:\tR$ {p1:.2f} to R$ {p2:.2f}'.format(p1=y_test.loc[sym,'Cotação pred']-stdDev_test,
                                                                       p2=y_test.loc[sym,'Cotação pred']+stdDev_test))
    
    
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
