import pandas as pd
import numpy as np
import yfinance as yf
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px

risk_free_return = 6.35
stockname = 'Tata Motors'
scrip = 'TATAMOTORS.NS'
temp = 'plotly_white'

def returns(df, name):
    df['Shifted Adj Close'] = df['Adj Close'].shift(periods = 1)
    df[f'{name} Return'] = (df['Close'] - df['Shifted Adj Close']) * 100 / df['Shifted Adj Close']
    df.dropna(axis = 0, inplace =True)
    return df[[f'{name} Return']]

stock = yf.download(scrip, start = '2010-01-01', progress=False, interval = '1wk')
market = yf.download('^NSEI', start = '2010-01-01', progress=False, interval = '1wk')

plot_df = pd.DataFrame()
plot_df[stockname] = stock['Adj Close']
plot_df['Market'] = market['Adj Close']

mkt_v_stock_line = px.line(np.log(plot_df), x = plot_df.index, y = plot_df.columns, labels = {'value' : 'log(Price)', 'variable' : 'Label'})
mkt_v_stock_line.layout.template = temp

stock_return = returns(stock, 'Stock')
market_return = returns(market, 'Market')

returns_df = pd.merge(market_return, stock_return, left_index = True, right_index = True, how = 'left')
returns_df['Excess Return'] = returns_df['Stock Return'] - risk_free_return

return_line = px.line(returns_df, x = returns_df.index, y = returns_df.columns, labels = {'value' : 'Return', 'variable' : 'Label'})
return_line.layout.template = temp
return_line.show()

mkt_v_exc = px.scatter(returns_df, x = 'Market Return', y = 'Excess Return')
mkt_v_exc.layout.template = temp

reg = px.scatter(returns_df, x = 'Market Return', y = 'Excess Return', trendline = 'ols')
reg.layout.template = temp
reg.data[1].name = 'Regression Line'
reg.data[1].showlegend = True
reg.data[1].line.color = 'orangered'
res = px.get_trendline_results(reg)
alpha = res.iloc[0]['px_fit_results'].params[0]
beta = res.iloc[0]['px_fit_results'].params[1]

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'CAPM'
server = app.server

app.layout = html.Div([html.H1('CAPM'),
                       html.Br(),
                       html.Div([html.H3('Performace'), dcc.Graph(id = 'mktvstock', figure = mkt_v_stock_line)]),
                       html.Br(),
                       html.Div([html.H3('Returns'), dcc.Graph(id = 'return', figure = return_line)]),
                       html.Br(),
                       html.Div([html.H3('Market Return vs Excess Return'), dcc.Graph(id = 'mktvexc', figure = mkt_v_exc)]),
                       html.Br(),
                       html.Div([html.H3('Regression Analysis'), html.H5('ri - rf = alpha + beta (rm - rf) + e'), dcc.Graph(id = 'regline', figure = reg)]),
                       html.Br(),
                       
                      ], 
                      style = {'width' : '75%', 'textAlign' : 'center', 'margin' : 'auto'}
                     )

if __name__ == '__main__':
    app.run_server()