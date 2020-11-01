# -*- coding: utf-8 -*-
"""
Main Script

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""


# TODO
# Interact with graph functions
# interact with logging functions

# TODO testes: BBAS3, ELET3, ABEV3


from FundamentusScraper import ScrapMarketData
from DataWrangling import WrangleModelingData
from DataModeling import PolynomialModeling
from GuiHandler import Window

import pandas as pd
from PyQt5.QtWidgets import *
import sys

# Run Application, Create the GUI
if __name__ == '__main__':

    # Start App
    if QApplication.instance():
        app = QApplication.instance()
    else:
        app = QApplication(sys.argv)

    # Start Window
    Gui = Window()
    
    app.setStyle('Fusion')
    app.exec_()
    sys.exit(app.exec_()) # Clean Exit


def StartBotCalculations(sym, Gui):

    corrThreshold = 0.38 # Correlation Threshold
    print('\nSelected Symbol is', sym)

    df_mkt = ScrapMarketData(sym) # Market DataFrame

    if type(df_mkt) != pd.core.frame.DataFrame:
        print('Invalid market dataset')
    else:
        df_model = WrangleModelingData(sym, df_mkt, corrThreshold) # Model DataFrame
        
        if df_model.shape[1] > 1:
            PolynomialModeling(sym, df_model) # Polynomial Modeling
        else:
            print('No valid dataset for modeling')
        