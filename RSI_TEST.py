# -*- coding: utf-8 -*-
"""
Created on Wed Jan  4 19:49:18 2023

@author: Krzychu
"""

import pandas as pd
import matplotlib.pyplot as plt
from pandas_datareader import data as pdr
import datetime as dt
import yfinance as yf
from matplotlib.pyplot import figure

pd.options.mode.chained_assignment = None  # default='warn' 
plt.style.use('default')   #styl wykresów


#1 Zmienne 
start = dt.datetime(2018,2,1)   #Początek badanego zakresu danych
end = dt.datetime(2023,9,6)   #Koniec badanego zakresu danych
rsi_lenght = 14 #Argument rsi (dla ilu okresów badane)

#2 Wczytanie danych z yahoo
company = ["^GSPC"]  #ticker z https://finance.yahoo.com/

yf.pdr_override()
df=pdr.get_data_yahoo(company, start, end)


