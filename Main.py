# -*- coding: utf-8 -*-
"""
Main Script

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""


# TODO testes: BBAS3, ELET3, ABEV3


from FundamentusScraper import ScrapMarketData
from DataWrangling import WrangleModelingData
from DataModeling import PolynomialModeling
from GuiHandler import *

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


# Start Calculations
def StartBotCalculations(sym, Gui):

    corrThreshold = 0.75 # Correlation Threshold
    df_mkt = ScrapMarketData(sym, Gui) # Market DataFrame

    if type(df_mkt) != pd.core.frame.DataFrame:
        Gui.AppendLog('* Market dataset is not valid. Analysis fineshed.')
    else:
        df_model = WrangleModelingData(sym, df_mkt, corrThreshold, Gui) # Model DataFrame
        
        if df_model.shape[1] > 1:
            PolynomialModeling(sym, df_model, Gui) # Polynomial Modeling
            Gui.AppendLog('Analysis concluded.')
        else:
            Gui.AppendLog('* Modeling dataset is not valid. Analysis fineshed.')
