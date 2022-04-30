import yfinance as yf
import pandas as pd

def getRealStock(data,stock):
    start = min(data['date']).strftime('%Y-%m-%d')
    end = max(data['date']-  pd.to_timedelta(1, unit='d')).strftime('%Y-%m-%d')
    stock_data = yf.download(stock,start,end)
    stock_data['date'] = stock_data.index
    stock_data['date'] = pd.to_datetime(stock_data['date'],utc=True).dt.normalize()
    stock_data['Adj Close'] = stock_data['Adj Close'].astype(int)
    stock_data['Adj Close'] = stock_data['Adj Close'].apply(lambda x: (x - min(stock_data['Adj Close'])) / (max(stock_data['Adj Close']) - min(stock_data['Adj Close'])) * 0.5)
    result_data = pd.merge(data,stock_data,on='date')
    result_data = result_data[['date','text_blob','vader_sentiment','Adj Close']].copy()
    return result_data