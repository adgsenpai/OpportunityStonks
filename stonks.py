import pandas as pd
import yfinance as yf
from yahoofinancials import YahooFinancials
import pandas as pd
import numpy as np
from forex_python.converter import CurrencyRates
import os, sys
import plotly.graph_objects as go
from tvDatafeed import TvDatafeed,Interval

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def GetUSDtoZAR():
    c = CurrencyRates()
    return c.convert('USD', 'ZAR', 1)
    
def GetStockHistory(Code):
    df = yf.download(Code+'.JO')
    df['Date'] = df.index
    return df

def EvaluateStock(StockCode):
    with HiddenPrints():
       data = GetStockHistory(StockCode)
    min = data['Close'].min()
    max = data['Close'].max()
    current = data['Close'].iloc[-1]
    return ('Could achieve '+str(round((1- (current/max)) * 100, 2)) + '% Growth from ' + str(current) + ' ZAR per share to ' + str(max) + ' ZAR per share')
