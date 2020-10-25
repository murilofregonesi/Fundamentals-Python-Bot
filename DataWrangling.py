# -*- coding: utf-8 -*-
"""
Data Wrangling

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

'''
TODO
1.  Manually analyze data, find correlations with price
    Either automate or standardize this procedure
    Define variables to be included into the modeling process
3.  Manually verify the nature of the correlation
    Either automate or standardize this procedure
    Define the modeling methods to be applied
4.  Review the DataFrame and drop or adapt significant missing values
'''

from FundamentusScraper import ScrapMarketData

sym = 'BBAS3' # Target Stock Symbol
df_mkt = ScrapMarketData(sym) # Market DataFrame

