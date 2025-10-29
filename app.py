import dash
import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output, State, callback

spacex_df = pd.read_csv("../spacex_launch_dash.csv")

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                 [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),

    html.Br(),

    dcc.Graph(id='pie-1'),

    dcc.RangeSlider(
        id='slider',
        min=0,
        max=10000,
        step=1000,
        marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
        value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()]
    ),

    dcc.Graph(id='scatter-1')
])

@app.callback(
    Output('pie-1', 'figure'),
    Output('scatter-1', 'figure'),
    Input('dropdown', 'value'),
    Input('slider', 'value')
)
def get_graphs(site, payload):
    if site == 'ALL':
        fig1 = px.pie(spacex_df, names='Launch Site', values='class', title='Total Success Launches by Site')
        df2 = spacex_df
    else:
        df2 = spacex_df[spacex_df['Launch Site'] == site]
        fig1 = px.pie(df2, names='class', title=f'Total Success vs Failure for site {site}')

    df2 = df2[(df2['Payload Mass (kg)'] >= payload[0]) & (df2['Payload Mass (kg)'] <= payload[1])]

    fig2 = px.scatter(df2, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                      title='Correlation between Payload and Success for all Sites')
    
    return fig1, fig2

if __name__ == '__main__':
    app.run(jupyter_mode='external')
