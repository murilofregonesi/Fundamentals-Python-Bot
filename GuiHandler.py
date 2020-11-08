# -*- coding: utf-8 -*-
"""
GUI Handler

Created on Oct 2020
@author: Murilo Fregonesi Falleiros
"""

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

class Window(QMainWindow):

    def __init__(self):
        super().__init__() # Window initialized as in parent

        # Window
        self.setWindowTitle('Fundamentals Python Bot')
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon('app_icon.png'))

        # Input
        self.startLabel = QLabel('Target Symbol', self)
        self.startLabel.setGeometry(QtCore.QRect(20, 10, 70, 20))

        self.startLine = QLineEdit(self)
        self.startLine.setGeometry(QtCore.QRect(20, 30, 91, 20))

        self.startBtn = QPushButton('Start Analysis', self)
        self.startBtn.setGeometry(QtCore.QRect(20, 60, 91, 40))
        self.startBtn.clicked.connect(self.__OnStartClick)

        # Logging
        self.logLabel = QLabel('Logging',self)
        self.logLabel.setGeometry(QtCore.QRect(150, 10, 47, 21))

        self.logPlain = QPlainTextEdit(self)
        self.logPlain.setGeometry(QtCore.QRect(150, 30, 350, 90))
        self.logPlain.setReadOnly(True)
        
        # Graphics
        self.plotLabel = QLabel('Market Distribution',self)
        self.plotLabel.setGeometry(QtCore.QRect(20, 120, 101, 21))

        # Others
        self.companyLabel = QLabel('M&N Investing\nhttps://linktr.ee/murilofregonesifalleiros',self)
        self.companyLabel.setGeometry(QtCore.QRect(20, 560, 800, 31))
        self.__SetPalette()
        
        self.show()

    def __SetPalette(self):

        palette = QPalette()
        brush = QBrush(QColor(112, 112, 112))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)

        brush = QBrush(QColor(112, 112, 112))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)

        brush = QBrush(QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)

        self.companyLabel.setPalette(palette)
        self.companyLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.companyLabel.setObjectName("companyLabel")

        self.menubar = QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 540, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

    def __OnStartClick(self):
        self.__sym = self.startLine.text().upper()
        self.ClearLog()
        self.AppendLog('Symbol for analysis ' + self.__sym)

        from Main import StartBotCalculations
        StartBotCalculations(self.__sym, self)

    def GetSymbol(self):
        return self.__sym

    def ClearLog(self):
        self.logPlain.clear()

    def AppendLog(self, text):
        self.logPlain.appendPlainText(text)


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class PlotCanvas(FigureCanvas):
    def __init__(self, parent):

        self.fig, self.ax = plt.subplots(figsize=(7.6, 4.1), dpi=100, clear=False)
        super().__init__(self.fig)
        
        self.setParent(parent)
        self.move(20, 140)
