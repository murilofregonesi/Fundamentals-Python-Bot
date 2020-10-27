# -*- coding: utf-8 -*-
"""
Main Script

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""


# TODO define script function, rename and create its interfaces
# Data Statistics
# Add return in Data modeling for receiving target data for evaluation
# maybe structure with all data at once


from FundamentusScraper import ScrapMarketData
from DataWrangling import WrangleModelingData
from DataModeling import PolynomialModeling

sym = 'BBAS3' # Target Stock Symbol
corrThreshold = 0.25 # Correlation Threshold

df_mkt = ScrapMarketData(sym) # Market DataFrame
try:
    if df_mkt <= 0:
        print('Invalid market dataset')
except:
    df_model = WrangleModelingData(sym, df_mkt, corrThreshold) # Model DataFrame
    PolynomialModeling(sym, df_model) # Polynomial Modeling
    