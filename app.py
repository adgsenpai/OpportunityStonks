import dash
from dash import dcc
from dash import html
import dash_dangerously_set_inner_html as override
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import stonks
import plotly.graph_objects as go

app = dash.Dash(__name__)


jsestonks = pd.read_csv('./research/notebookplayground/StonkCodes.csv')
jsestonksoptions = []
for i, row in jsestonks.iterrows():
    jsestonksoptions.append({'label': row['Company'], 'value': row['Code']})

app.layout = html.Div([
    html.Div([(override.DangerouslySetInnerHTML('''<h1>    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1" id="Capa_1" x="0px" y="0px" viewBox="0 0 386.651 386.651" style="enable-background:new 0 0 386.651 386.651;" xml:space="preserve"  width="10%" height="10%"><g>	<path d="M342.367,135.781c-2.674-1.367-5.889-1.122-8.324,0.635l-138.556,99.968l-89.233-83.725   c-3.032-2.844-7.736-2.892-10.826-0.112l-74.395,66.959c-1.685,1.518-2.648,3.679-2.648,5.946v91.451c0,4.418,3.582,8,8,8h312.339   c4.418,0,8-3.582,8-8v-174C346.724,139.899,345.041,137.149,342.367,135.781z M53.507,308.903H34.385v-79.889l19.122-17.211   V308.903z M88.045,308.903H69.507v-111.5l18.538-16.685V308.903z M122.582,308.903h-18.538V172.526l18.538,17.393V308.903z    M157.12,308.903h-18.538V204.931l18.538,17.394V308.903z M192.015,308.903H173.12v-71.565l16.227,15.226   c0.791,0.741,1.702,1.288,2.667,1.65V308.903z M226.91,308.903h-18.896v-61.828l18.896-13.634V308.903z M261.806,308.903H242.91   v-87.006l18.895-13.633V308.903z M296.701,308.903h-18.896V196.72l18.896-13.634V308.903z M330.724,308.903h-18.022v-137.36   l18.022-13.003V308.903z"/>	<path d="M385.375,65.087c-1.439-2.148-3.904-3.404-6.461-3.337l-50.696,1.368c-3.471,0.094-6.429,2.547-7.161,5.941   c-0.732,3.395,0.95,6.85,4.074,8.366l11.846,5.75L196.96,183.012l-95.409-86.504c-4.738-4.296-11.955-4.322-16.723-0.062   L4.173,168.491c-5.149,4.599-5.594,12.501-0.995,17.649c4.598,5.148,12.499,5.594,17.649,0.995l72.265-64.55l94.533,85.709   c2.369,2.147,5.376,3.239,8.398,3.239c2.532,0,5.074-0.767,7.255-2.322L350.82,104.01l0.701,11.074   c0.22,3.464,2.777,6.329,6.193,6.939c0.444,0.079,0.889,0.118,1.328,0.118c2.938,0,5.662-1.724,6.885-4.483l20.077-45.327   C387.052,69.968,386.815,67.234,385.375,65.087z"/></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g><g></g></svg>    Opportunity Stonks App</h1><br>''')),
    dcc.Dropdown(id='company-dropdown',
    options=jsestonksoptions,
    searchable=True,placeholder="Search for a company"
),
override.DangerouslySetInnerHTML('<br>'),
dcc.Graph(id='stock-graph'),
],className="row mt-4")],className="container-fluid py-4")

@app.callback(
    Output('stock-graph', 'figure'),
    Input('company-dropdown', 'value')
)
def update_output(value):
    if value == None:
        raise dash.exceptions.PreventUpdate
    else:
        try:
            df = stonks.GetStockHistory(value)
            fig = px.line(df, x="Date", y="Close",title='Stock Price of '+value)
            fig.update_layout(transition_duration=500)
            return fig
        except:
            raise dash.exceptions.PreventUpdate
        
   
    


if __name__ == '__main__':
    app.run_server(debug=True)