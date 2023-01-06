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
import pandas_ta as ta

pd.options.mode.chained_assignment = None  # default='warn' 
plt.style.use('default')   #styl wykresów


#1 Zmienne 
start = dt.datetime(2000,2,1)   #Początek badanego zakresu danych
end = dt.datetime(2023,9,6)   #Koniec badanego zakresu danych
rsi_lenght = 14 #Argument rsi (dla ilu okresów badane)
min_rsi = 30
max_rsi = 70

#2 Wczytanie danych z yahoo
company = ["^GSPC"]  #ticker z https://finance.yahoo.com/

yf.pdr_override()
df = pdr.get_data_yahoo(company, start, end)  #Stworzenie df z danych 
df.reset_index(inplace=True)  #Resetuje indeksy ( i je tworzy)


#3 Obliczanie wskaźnika RSI
df['Rsi']=ta.rsi(df["Close"], length=rsi_lenght) #RSI

#4 Strategia RSI
"""Zakup aktywów za cenę Close, gdy w danym dniu RSI było mniejsze niż 30.
sprzedaż aktywów, gdy RSI>70. Inwestujemy za każdym razem stałą kwotę. Zysk wyrażony
zostanie w procentach (procent skumulowany zysków i strat ze wszystkich tranzakcji"""


trans = []
trans_sum = [0]  
buy = 0
sell = 0
sell_dates = []
close = []

for i in range(len(df)):
    if df['Rsi'][i]<30 and buy==0: #Kupno
        buy = df['Close'][i]
        
    elif df['Rsi'][i]>70 and buy!=0: #Sprzedaż 
        sell = df['Close'][i]
        
        profit = ((sell - buy)/buy) * 100  #Profit wyrażony w procentach    
        trans.append(profit) #lista profitóW
        trans_sum.append(trans_sum[-1]+profit) #dodaje profit do listy skumulowanych profitów 
        sell_dates.append(df['Date'][i]) #dodaje datę do listy dat
        close.append(df["Close"][i])
        buy = 0 #resetuje wartosc buy


#5 Interpretacja wyników

print(trans_sum[-1]) #drukuje procent skumulowany


trans_sum.pop(0) #usuwa pierwszą (zerową) pozycję z listy procentu skomulowanego

fig,ax = plt.subplots() # Umożliwia stworzenie wykresu z dwoma osiami Y


ax.plot(sell_dates,trans_sum, color="red", marker="o") #tworzy wykres zysku skumulowanego


ax.set_xlabel("data", fontsize = 14) # Tytuł osi X

plt.xticks(rotation=90) #obraca podpisy osi X o 90 stopni

ax.set_ylabel("zysk [%]", color="red", fontsize=14) #Tworzy podpis osi Y

plt.grid() #Tworzy siatkę na wykresie


ax2=ax.twinx()   #Tworzy drugą os Y

ax2.plot(sell_dates, close,color="blue",marker="o") #Wykres dla drugiej osi, przedstawia ruch ceny wybranej spółki
ax2.set_ylabel("Close",color="blue",fontsize=14) #Podpisuje os Y

plt.title(company[0]) #Tytuł wykresu


plt.savefig(company[0]+'.png') #Zapisuje wykres
plt.show() #Pokazuje wykres


