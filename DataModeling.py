# -*- coding: utf-8 -*-
"""
Data Modeling

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

def PolynomialModeling(sym, df_model, Gui):

    #%% Polynomial Modeling
    
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn import linear_model
    from sklearn.model_selection import train_test_split
    
    # Set target symbol apart
    X_sym = df_model.loc[sym][1:]
    y_sym = df_model.loc[sym][0]
    
    # Group modeling datasets
    X = df_model.iloc[:,1:].drop(sym,axis=0)
    y = df_model.iloc[:,0].drop(sym,axis=0)
    
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
    Gui.AppendLog('Selected polynomial degree {}'.format(polyDg))
    
    # Create the final model
    poly = PolynomialFeatures(degree = polyDg)
    X_train_tr = poly.fit_transform(X_train)
    
    poly_model = linear_model.LinearRegression()
    poly_model.fit(X_train_tr, y_train)
    
    # Insert target symbol to the test set
    X_test = pd.concat([pd.DataFrame(X_sym).transpose(), X_test])
    y_test = pd.concat([pd.Series(y_sym), y_test])
    y_test.index.array[0] = sym
    
    # Apply the model to the test set
    X_test_tr = poly.fit_transform(X_test)
    y_pred = poly_model.predict(X_test_tr)
    
    y_train_pred = poly_model.predict(X_train_tr)
    
    # Predictions Standard Deviation
    stdDev_test = np.std(y_test - y_pred)
    stdDev_train = np.std(y_train - y_train_pred)
    
    Gui.AppendLog('\nTest Standard Deviation {dev:.2f}'.format(dev=stdDev_test))
    Gui.AppendLog('Train Standard Deviation {dev:.2f}'.format(dev=stdDev_train))
    
    # Plot the results
    import matplotlib.pyplot as plt
    from GuiHandler import PlotCanvas

    graph = PlotCanvas(Gui) # Start a Canvas

    graph.ax.scatter(X_test.index, y_test)
    graph.ax.scatter(X_test.index, y_pred)
    graph.ax.scatter(X_train.index, y_train)
    graph.ax.scatter(X_train.index, y_train_pred)

    plt.ylabel('Price (R$)')
    plt.grid()
    plt.ylim(ymin=0)
    plt.legend(['Actual (test)', 'Prediction (test)',
                'Actual (train)', 'Prediction (train)'])
    plt.xticks(rotation=90)
    plt.errorbar(X_test.index, y_pred, yerr = stdDev_test, linestyle='None',
                 ecolor='darkorange', capthick=3)
    plt.errorbar(X_train.index, y_train_pred, yerr = stdDev_train, linestyle='None',
                 ecolor='r', capthick=3)

    plt.subplots_adjust(top = 0.99, bottom = 0.18, right = 0.99, left = 0.08, hspace = 0, wspace = 0)
    graph.show()
    