import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots

complete = pd.read_csv('result/complete.csv')
summary = pd.read_csv('result/summary.csv')

summary_table = go.Figure(data = [go.Table(header = dict(values = list(summary.columns)),
                          cells = dict(values = [summary['Class'], summary['Total Cost'], summary['Cost Percentage'], summary['Frequency'], summary['Share Percentage']]))])
summary_table.update_layout(height = 300);

pareto = px.line(complete, x = 'CummulativeDP', y = 'CummulativeCP', color = 'Class')

specs = [[{'type' : 'domain'}, {'type' : 'domain'}]]
donut = make_subplots(rows = 1, cols = 2, specs = specs)
donut.add_trace(go.Pie(labels = summary['Class'], values = summary['Cost Percentage'], title = 'Cost %'), 1, 1)
donut.update_traces(hole = .75, hoverinfo = "label+percent+name")
donut.add_trace(go.Pie(labels = summary['Class'], values = summary['Share Percentage'], title = 'Share %'), 1, 2)
donut.update_traces(hole = .75, hoverinfo = "label+percent+name")
donut = go.Figure(donut)

items = go.Figure(data = [go.Table(header = dict(values = list(summary['Class'])),
                  cells=dict(values=[complete.query('Class=="A"')['Item-code'],
                                     complete.query('Class=="B"')['Item-code'],
                                     complete.query('Class=="C"')['Item-code']]))])
items.update_layout(height = 800);

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'ABC Classification'
server = app.server

app.layout = html.Div([html.H1('ABC Classification'),
                       html.Br(),
                       html.Div([html.H3('Summary Table'), dcc.Graph(id = 'summary', figure = summary_table)]),
                       html.Br(),
                       html.Div([html.H3('Pareto Curve'), dcc.Graph(id = 'pareto', figure = pareto)]),
                       html.Br(),
                       html.Div([html.H3('Donut Plot'), dcc.Graph(id = 'donut', figure = donut)]),
                       html.Br(),
                       html.Div([html.H3('Item Table'), dcc.Graph(id = 'items', figure = items)])
                      ], 
                      style = {'width' : '75%', 'textAlign' : 'center', 'margin' : 'auto'}
                     )

if __name__ == '__main__':
    app.run_server()