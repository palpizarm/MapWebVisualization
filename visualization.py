import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
#general configuration

# import data
data_countries = pd.read_csv(r"data/World_Happinnes.csv")


var = {1: 'Score', 2: 'GDP per capita', 3: 'Social support', 4: 'Freedom to make life choice',
       5: 'Generosity', 6: 'Perceptions of corruption'}


# App layout
app.layout = html.Div([
    html.Div(children =[
        html.H1("Indice de Felicidad 2019", style={
                'text-align': 'left', 'color': 'blue'}),
    ], style={'display': 'inline-block'}),
    html.Div(children=[
        html.Div(children= [ html.Label(["Seleccione la variable", dcc.Dropdown(
            id="select_var",
            options=[
                {"label": "Score", "value": 1},
                {"label": "GDP per capita", "value": 2},
                {"label": "Social support", "value": 3},
                {"label": "Freedom to make life choices", "value": 4},
                {"label": "Generosity", "value": 5},
                {"label": "Perceptions of corruption", "value": 6},
            ],style={'width':'50%'},
            value=1,
            searchable=False,
            clearable=False,

        )]),
            html.Div(children=[
                html.Button('Distribución por Continente', id='buttonC'),
                html.Button('Distribución por Pais', id='buttonP'),
            ], style={'display':'inline-block', 'float':'center'}),
        ]),
        html.Div([
            html.Div([
                dcc.Graph(id='map', config={'scrollZoom': True}),
            ], style={'width': '100%', 'display': 'inline-block'}),
            html.Div(children=[
                html.Div([
                    html.H1("Indice del planeta feliz", style={
                        'text-align': 'center', 'color': 'blue'}),
                ]),
                html.Div(children=[
                    html.P("El índice global de felicidad es una publicación anual de las Naciones Unidas que mide la felicidad en 157 países, basándose en diversos factores, como el PIB per cápita," +
                       "la esperanza de vida saludable y el apoyo social, la primera que que se realizo el estudio fue en el 2012"),
                ], style={'width':'100%', 'display':'inline-block'}),
                html.Div(children=[
                    html.Div([
                        dcc.Graph(id='bar')
                    ], style={'float': 'left', 'width': '60%'}),
                    html.Div([
                    dcc.Markdown('''
                       ### Se utilizan criterios como:
                       * PIB per cápita.
                       * Apoyo social.
                       * Esperanza de vida saludable.
                       * Libertad para tomar decisiones en la vida.
                       * Generosidad.
                       * Percepciones de corrupción.
                    ''')
                    ], style={'float': 'right', 'width': '40%'})
                ], style={'display': 'inline-block', 'width': '100%'}),
                html.Div([
                    html.P("El promedio para 2019 fue de 5.42 points.El valor más alto fue en Finlandia: 7.77 points y el valor más bajo fue en Rep. Centroafricana: 3.08 points.")
                ])
            ], style={'width': '100%', 'display': 'inline-block'})
        ])
    ])
])

@app.callback(
    [Output('select_var','disabled'),
    Output('map', 'figure'),
    Output('bar', 'figure')],
    [Input('select_var', 'value'),
    Input('buttonC', 'n_clicks'),
    Input('buttonP', 'n_clicks')])

def update_graph(select_var, bt1,bt2):
    charts= [False]
    main_var = var[select_var]
    data_bar = data_countries[:10]

    bt = [p['prop_id'] for p in dash.callback_context.triggered][0]
    context = 'Pais'
    if 'buttonC' in bt:
        context = 'Continente'
        charts[0] = True
    elif 'buttonP' in bt:
        context == 'Pais'
        charts[0] = False
    title = 'Distribución del indice de felicadad 2019 por ' + main_var + ' según ' + context

    
    if context == 'Continente':
        # Choropleth map
        charts.append(px.choropleth(
            data_frame=data_countries,
            projection='equirectangular',
            locationmode='country names',
            locations=data_countries['Country or region'],
            color='Score by Continent',
            hover_name = 'Continent',
            color_continuous_scale=px.colors.sequential.Viridis,
            labels={'Score by Continent':'Score'},
            scope='world',
            #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
        ))
    elif context == 'Pais':
        # Choropleth map
        charts.append(px.choropleth(
            data_frame=data_countries,
            locationmode='country names',
            projection='equirectangular',
            locations=data_countries['Country or region'],
            color=main_var,
            hover_name='Country or region',
            hover_data=['Continent', main_var],
            color_continuous_scale=px.colors.sequential.Viridis,
            scope='world',
            #zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
            ))
    # Bar chart
    charts.append(px.bar(
        data_bar,
        x='Country or region', 
        y=['GDP per capita', 'Social support',	'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'],
        title='Top 10 de los paises con mejor puntuación'
    ))
    charts[1].update_layout(margin={"r":0,"t":0,"l":0,"b":0},)

    return charts


if __name__ == '__main__':
    app.run_server(debug=True)
