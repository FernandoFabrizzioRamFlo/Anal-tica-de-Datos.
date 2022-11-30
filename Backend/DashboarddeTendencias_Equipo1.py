import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_excel("Data_base.xlsx")

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

app.layout = \
dbc.Container\
([
      html.Br(), #Titulo
      dbc.Row([dbc.Col([html.H1('Trend Dashboard', className='text-center text primary, mb-3')])]),
      
      html.Br(),
      dbc.Row([ #Primera fila (Dropdowns)
      dbc.Col([dcc.Dropdown(id='Familia Dropdown',
                       options=[{'label': i,'value': i}
                                for i in df['Familia'].unique()],
                       placeholder = 'select a Family',
                       #value='4W3G80'
                       )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='Refrigerante Dropdown',
                       options=[{'label': i,'value': i}
                                for i in df['Refrigerant'].unique()],
                       placeholder = 'select a Refrigerant',
                       #value='R600'
                       )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='x_dropdown',
                            options=[{'label': i, 'value':i}
                                     for i in df.columns],
                            placeholder = 'Select an X Variable',
                            #value='FC3 Temp A°F'
                            )],
              width=3),
      
      dbc.Col([dcc.Dropdown(id='y_dropdown',
                            options=[{'label': i, 'value':i}
                                     for i in df.columns],
                            placeholder = 'select a Y Variable',
                            #value='FC2 Temp A°F'
                            )],
              width=3)
      ]), #Fin de primera fila
      
      html.Br(),
      dbc.Row([dbc.Col([dcc.Graph(id='regression', style={'height':550})],width=12)]),
      
      html.Br(),
      dbc.Row([
          dbc.Col([dcc.Graph(id='Count', style={'height':200})],width=6),
          dbc.Col([dcc.Graph(id='Corr', style={'height':200})],width=6)
          ])
])


@app.callback( #Grafica
    Output(component_id='regression', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value'),
    Input(component_id='y_dropdown', component_property= 'value')
)

def indicadores_pm(selected_family, selected_refrigerant, x_var, y_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
           
    data = px.scatter(filtered_df, x=x_var,y=y_var,template = 'plotly_white', trendline='ols')
    
    return data

@app.callback( #Count
    Output(component_id='Count', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value')
)
def contador(selected_family, selected_refrigerant, x_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    fig = go.Figure()

    fig.add_trace(go.Indicator(
        value = filtered_df[x_var].count(),
        number = {"font":{"size":90}},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Number of Registries","font":{"size":20}}))
    
    return fig
 
 
@app.callback( #corr
    Output(component_id='Corr', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property='value'),
    Input(component_id='x_dropdown', component_property= 'value'),
    Input(component_id='y_dropdown', component_property= 'value')
)

def corr(selected_family, selected_refrigerant, x_var, y_var):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    fig1 = go.Figure()

    fig1.add_trace(go.Indicator(
        value = np.corrcoef(filtered_df[x_var], filtered_df[y_var])[0,1],
        gauge = {
            'axis': {'visible': False}},
        number = {"font":{"size":90}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Pearson Correlation","font":{"size":20}}))
    
    return fig1

  
if __name__ == '__main__':
    app.run_server()