# -*- coding: utf-8 -*-
"""
Data Wrangling

@input: Target Symbol (string)
        Market Data (DataFrame)
        Correlation Threshold (float)
@output: Modeling Data (DataFrame)

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

def WrangleModelingData(sym, df_mkt, corrThreshold):

    #%% Prepare Modeling DataFrame
    
    import numpy as np
    import pandas as pd
    
    # Remove unavailable columns on Target Stock
    drop_list = df_mkt.loc[sym] == 0
    for i, item in enumerate(drop_list):
        if(item):
            df_mkt = df_mkt.drop(drop_list.index[i], axis='columns')
    
    # Find features correlation with price
    df_corr = pd.DataFrame(df_mkt.corr()['Cotação'])
    df_corr['CorrAbs'] = df_corr['Cotação'].abs()
    
    df_corr.sort_values(by='CorrAbs', axis=0, ascending=False, inplace=True)
    df_corr.columns = ['Corr','CorrAbs']
    print('\nCorrelations:')
    print(df_corr['Corr'])
    
    # Select Model Features
    df_select = df_corr[df_corr['CorrAbs'] > corrThreshold]
    df_model = df_mkt[df_select.index]
    print('\nConsidered Features:',df_model.columns[1:])
    
    # Remove Symbols with missing main features data
    df_model = df_model.replace(0,np.nan)
    df_model = df_model.dropna()
    
    if df_model.shape[1] > 2:
    
        import matplotlib.pyplot as plt
        
        y = df_model['Cotação']
        
        fig = plt.figure()
        fig.add_subplot(1,2,1)
        plt.scatter(df_model.iloc[:,1], y)
        plt.xlabel(df_model.columns[1])
        plt.ylabel('Price (R$)')
        
        fig.add_subplot(1,2,2)
        plt.scatter(df_model.iloc[:,2], y)
        plt.xlabel(df_model.columns[2])
        plt.ylabel('Price (R$)')
        
    return df_model
