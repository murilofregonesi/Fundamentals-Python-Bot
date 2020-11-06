# -*- coding: utf-8 -*-
"""
Data Wrangling

@input: Target Symbol (string)
        Market Data (DataFrame)
        Correlation Threshold (float)
        GUI (Window)
@output: Modeling Data (DataFrame)

Created on Nov 2020
@author: Murilo Fregonesi Falleiros
"""

def WrangleModelingData(sym, df_mkt, corrThreshold, Gui):

    #%% Prepare Modeling DataFrame

    import numpy as np
    import pandas as pd

    # Remove unavailable columns on Target Stock
    drop_list = df_mkt.loc[sym] == 0
    for i, item in enumerate(drop_list):
        if(item):
            df_mkt = df_mkt.drop(drop_list.index[i], axis='columns')

    # Find features correlation with P/VP (Target variable)
    df_corr = pd.DataFrame(df_mkt.corr()['P/VP'])
    df_corr['CorrAbs'] = df_corr['P/VP'].abs()

    df_corr.sort_values(by='CorrAbs', axis=0, ascending=False, inplace=True)
    df_corr.columns = ['Corr','CorrAbs']
    
    Gui.AppendLog('\nCorrelations:')
    Gui.AppendLog(str(df_corr['Corr']))

    # Select Model Features
    df_select = df_corr[df_corr['CorrAbs'] > corrThreshold]
    df_model = df_mkt[df_select.index]

    Gui.AppendLog('\nConsidered Features:' + str(df_model.columns[1:]))

    # Repair price column if necessary
    if 'Cotação' not in df_model:
        df_model['Cotação'] = df_mkt.loc[df_model.index, 'Cotação']
            
    # Remove Symbols with missing main features data
    df_model = df_model.replace(0,np.nan)
    df_model = df_model.dropna()

    return df_model
