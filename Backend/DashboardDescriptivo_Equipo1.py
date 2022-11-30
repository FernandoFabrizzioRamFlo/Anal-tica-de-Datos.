# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go

df = pd.read_excel("Data_base.xlsx")

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

app.layout = \
dbc.Container\
([
      html.Br(), #Titulo
      dbc.Row([dbc.Col([html.H1('Descriptive Dashboard', className='text-center text primary, mb-3')])]),
      
      html.Br(),
      
      dbc.Row([ #Primera fila (Dropdowns)
      dbc.Col([dcc.Dropdown(id='Familia Dropdown',
                            options=[{'label': i,'value': i} for i in df['Familia'].unique()],
                            placeholder = 'Select a Family',
                            #value='4W3G80',
                        #label ="Dropdown Menu",
                        #toggle_style = {color : "primary"},
                        clearable = True,
                        )]
               ,width=6),
      
       dbc.Col([dcc.Dropdown(id='Refrigerante Dropdown',
                        options=[{'label': i,'value': i}
                                 for i in df['Refrigerant'].unique()],
                        placeholder = 'Select a Refrigerant',
                        clearable = True,
                        #value='R600'
                        )]
               ,width=6),
      
      #dbc.Col([dcc.Graph(id='CPK')],width=4)
      
      # dbc.Col([dcc.Dropdown(id='Unit type Dropdown',
      #                  options=[{'label': i,'value': i}
      #                           for i in df['E-star/Std.'].unique()],
      #                  value='EMB')],width=3),
      ]),
      
      html.Br(),
      dbc.Row([ #Subtitulos
          dbc.Col([html.H4('Performance Percentages', className='text-center text primary, mb-3')],width=6),
          dbc.Col([html.H4('Temperatures Averages', className='text-center text primary, mb-3')],width=6)
          ]),
      
      html.Br(),
      dbc.Row([ #Fila de KPIs perf, Grafica de columnas, KPIs de RC, KPIs de FC
          dbc.Col([dcc.Graph(id='Performance KPIs')],width=3),
          dbc.Col([dcc.Graph(id='Temp Bar')], width=3),
          dbc.Col([dcc.Graph(id='RC KPIs')], width=3),
          dbc.Col([dcc.Graph(id='FC KPIs')], width=3)
          ]),
      
      html.Br(),
      dbc.Row([ # graficas de barras compresor vs below rating point, Histograma RC, Histograma FC
         dbc.Col([dcc.Graph(id='temp-comp')], width=6),
         dbc.Col([dcc.Graph(id='histograma RC')], width=3),
         dbc.Col([dcc.Graph(id='histograma FC')], width=3)
       ])      
])

@app.callback( #Performance KPIS
    Output(component_id='Performance KPIs', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property= 'value')
)

def indicadores_pm(selected_family, selected_refrigerant):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    usl = (filtered_df['Target'].iloc[-1]*1.03)
    X = (filtered_df['Energy Consumed (kWh/yr)'].tail(15).mean())
    desvest = (filtered_df['Energy Consumed (kWh/yr)'].tail(15).std())
    
    indicators_pm = go.Figure()
    #indicators_pm.layout.template = CHART_THEME

    indicators_pm.add_trace(go.Indicator(
        #value = filtered_df['% Run Time (M/M)'].count(),
        value = (usl-X)/(3*desvest),
        number = { "font":{"size":30}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "CPK","font":{"size":20}}))

    indicators_pm.add_trace(go.Indicator(
        value = len(filtered_df[(filtered_df['Aprobacion de Energia por Año'] == 'Aprobado')])/len(filtered_df)*100,
        number = {'suffix': "%","font":{"size":30}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': 0},
        title = {'text': "Approved Energy Consumption","font":{"size":20}}))

    indicators_pm.add_trace(go.Indicator(
        value = len(filtered_df[(filtered_df['Aprobacion RC'] == 'Aprobada')])/len(filtered_df)*100,
        number = {'suffix': "%","font":{"size":30}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 1, 'column': 0},
        title = {'text': " Approved RC Temperatures","font":{"size":20}}))
    
    indicators_pm.add_trace(go.Indicator(
        value = len(filtered_df[(filtered_df['Aprobacion FC'] == 'Aprobada')])/len(filtered_df)*100,
       number = {'suffix': "%","font":{"size":30}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 2, 'column': 0},
        title = {'text': " Approved FC Temperatures","font":{"size":20}}))
    
    indicators_pm.add_trace(go.Indicator(
        value = filtered_df['% Run Time (M/M)'].count(),
       number = {"font":{"size":35}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 4, 'column': 0},
        title = {'text': "# Of Tests","font":{"size":20}}))
    
    return indicators_pm.update_layout(
        grid = {'rows': 5, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30))

@app.callback( #Grafica de columnas de energía
    Output(component_id='Temp Bar', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property= 'value')
)
def column_chart(selected_family, selected_refrigerant):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    df2 = pd.DataFrame(filtered_df['Aprobacion de Energia por Año'].value_counts()).reset_index()
    fig = px.bar(
        df2,
        x = 'index',
        y = 'Aprobacion de Energia por Año',
        template = 'plotly_white',
        title = 'Anual Energy Consumption',
        #width = 800,
        labels = {'index':'','Aprobacion de Energia por Año':'Count'}
        )
    
    return fig

@app.callback( #RC KPIs
    Output(component_id='RC KPIs', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property= 'value')
)
def RC_KPIs(selected_family, selected_refrigerant):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    indicators_rc = go.Figure()
    #indicators_rc.layout.template = CHART_THEME
    
    indicators_rc.add_trace(go.Indicator(
        value= filtered_df['RC Temp Average A°F (M/M)'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'position':"top",'reference': 10},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': 0},
        title = {'text': "Avg RC Temperature","font":{"size":20}}))
    
    indicators_rc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['RC1 Temp °F'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['RC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 1, 'column': 0},
        title = {'text': "Avg RC1 Temperature","font":{"size":20}}))
    
    indicators_rc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['RC2 Temp A°F'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['RC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 2, 'column': 0},
        title = {'text': "Avg RC2 Temperature","font":{"size":20}}))
    
    indicators_rc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['RC3 Temp A°F'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['RC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Avg RC3 Temperature","font":{"size":20}}))
    
    
    #indicators_rc1.update_layout(paper_bgcolor = "lightgray") Ponerle color a la carta
    # Creo que no se puede poner un delta ya que todos los indicadores estan bjo una sola carta, para poder ponerlo se ocuparia una carta por c/u
    
    return indicators_rc.update_layout(
        grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30))
    
@app.callback( #FC KPIs
    Output(component_id='FC KPIs', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property= 'value')
)
def FC_KPIs(selected_family, selected_refrigerant):
    
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    
    indicators_fc = go.Figure()
    #indicators_fc.layout.template = CHART_THEME
    
    indicators_fc.add_trace(go.Indicator(
        value= filtered_df['FC Temp Average A°F (M/M)'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': 0},
        title = {'text': "Avg FC Temperature","font":{"size":20}}))
    
    indicators_fc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['FC1 Temp A°F'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['FC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 1, 'column': 0},
        title = {'text': "Avg FC1 Temperature","font":{"size":20}}))
    
    indicators_fc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['FC2 Temp A°F'].mean(),
       number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['FC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 2, 'column': 0},
        title = {'text': "Avg FC2 Temperature","font":{"size":20}}))
    
    indicators_fc.add_trace(go.Indicator(
        mode='number+delta',
        value= filtered_df['FC3 Temp A°F'].mean(),
        number = {'suffix': " ° F ", "font":{"size":30}},
        delta = {'reference': filtered_df['FC Temp Average A°F (M/M)'].mean()},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 3, 'column': 0},
        title = {'text': "Avg FC3 Temperature","font":{"size":20}}))
    
    return indicators_fc.update_layout(
        grid = {'rows': 4, 'columns': 1, 'pattern': "independent"},
        margin=dict(l=50, r=50, t=30, b=30))

@app.callback( #Comparación de compresores
    Output(component_id='temp-comp', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'),
    Input(component_id='Refrigerante Dropdown', component_property= 'value') #poner otro input para el dropdown de refrigerante
)
def update_bar(selected_family, selected_refrigerant):
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    bar_fig = px.bar(filtered_df,
                      x=filtered_df.groupby(['Compressor'])['% Below Rating Point'].median(),
                      height = 275,
                      y=filtered_df['Compressor'].unique(), orientation='h',
                      labels = {'index':'Categorias','Aprobacion de Energia por Año':'Conteo'},
                      template = 'plotly_white',
                      
                      #color_continuous_scale = px.colors.sequential.Yl0rRd,
                      title='% Below Rating Point per Compressor'
                      )
    bar_fig.update_layout(
        title_x=0.5,
        xaxis_title="% Below Rating Point",
        yaxis_title="Compressors",
        )
    
    return bar_fig

@app.callback(
    Output(component_id='histograma RC', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'), 
    Input(component_id='Refrigerante Dropdown', component_property='value')
)
def update_hist_rc(selected_family,selected_refrigerant):
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    hist_rc = px.histogram(filtered_df, nbins=4,
                           x = "RC Temp Average A°F (M/M)",
                           template = 'plotly_white',
                           height = 275,
                           title='RC Temp Avg Histogram °F (M/M)')
    return hist_rc

@app.callback(
    Output(component_id='histograma FC', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'), 
    Input(component_id='Refrigerante Dropdown', component_property='value')
)
def update_hist_fc(selected_family,selected_refrigerant):
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    hist_fc = px.histogram(filtered_df, nbins=4,
                           x = "FC Temp Average A°F (M/M)",
                           template = 'plotly_white',
                           height = 275,
                           title='FC Temp Avg Histogram °F (M/M)')
    return hist_fc

'''
@app.callback(
    Output(component_id='CPK', component_property='figure'),
    Input(component_id='Familia Dropdown', component_property='value'), 
    Input(component_id='Refrigerante Dropdown', component_property='value')
)
def cpk(selected_family, selected_refrigerant):
    filtered_df = df[(df['Familia'] == selected_family) & (df['Refrigerant'] == selected_refrigerant)]
    usl = (filtered_df['Target'].iloc[-1]*1.03)
    X = (filtered_df['Energy Consumed (kWh/yr)'].tail(15).mean())
    desvest = (filtered_df['Energy Consumed (kWh/yr)'].tail(15).std())
        
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        value = (usl-X)/(3*desvest),
        delta = {'reference': 0},
        gauge = {
            'axis': {'visible': False}},
        domain = {'row': 0, 'column': 0},
        title = {'text': "CPK"},
        height=100))
    
    return fig.show()
'''

if __name__ == '__main__':
    app.run_server(port=8051)