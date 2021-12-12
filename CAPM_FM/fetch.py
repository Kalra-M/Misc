import yfinance as yf
import pandas as pd

stock_name = 'Tata Motors'
stock_name_yf = 'TATAMOTORS.NS'

stock = yf.download(stock_name_yf, start = '2010-01-01', progress=False, interval = '1wk')
market = yf.download('^NSEI', start = '2010-01-01', progress=False, interval = '1wk')

df = pd.merge(market, stock, left_index = True, right_index = True, how = 'left', suffixes = ('_market', '_stock'))

df.rename(columns = {'Adj Close_market' : 'Market', 'Adj Close_stock' : 'Stock', 'Close_market' : 'Stock (Close + Dividend'}, inplace = True)

df[['Market', 'Stock', 'Stock (Close + Dividend']].to_excel(f'{stock_name}.xlsx', sheet_name = f'{stock_name}')
