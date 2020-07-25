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

# images

image_filename = 'data/happy.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# import and work on data
data = pd.read_csv(r"data/World_Happinnes.csv")

var = {1: 'Score', 2: 'GDP per capita', 3: 'Social support', 4: 'Freedom to make life choice',
       5: 'Generosity', 6: 'Perceptions of corruption'}

"""data.groupby(['rank', 'Score', 'Country or region', 'GDP per capita', 'Social support',
                   'Freedom to make life choices', 'Generosity', 'Perceptions of corruption', ])"""

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Indice de Felicidad 2019", style={
                'text-align': 'left', 'color': 'blue'}),
    ], className='row'),

    html.Div([
        html.Div(html.Label(["Seleccione la variable", dcc.Dropdown(
            id="select_var",
            options=[
                {"label": "Score", "value": 1},
                {"label": "GDP per capita", "value": 2},
                {"label": "Social support", "value": 3},
                {"label": "Freedom to make life choices", "value": 4},
                {"label": "Generosity", "value": 5},
                {"label": "Perceptions of corruption", "value": 6}],
            style={'width': '40%', 'display': 'block'},
            value=1,
            multi=False
        )]), className='row'),

        html.Div([
            html.Div([
                dcc.Graph(id='map'),
            ], className='row wind-speed-row'),
            html.Div([
                html.Div([
                    html.H1("Indice del planeta feliz", style={
                        'text-align': 'center', 'color': 'blue'}),
                ], className='row'),
                html.Div([
                    html.Div([
                        dcc.Graph(id='bar'),
                    ], className='two columns'),
                    html.Div([
                        html.P("El índice global de felicidad es una publicación anual de las Naciones Unidas que mide la felicidad en 157 países, basándose en diversos factores, como el PIB per cápita," +
                           "la esperanza de vida saludable y el apoyo social, la primera que que se realizo el estudio fue en el 2012"),
                    ], className='two columns'),
                ], className='row'),
                html.Div([
                    html.P(
                        "El promedio para 2019 fue de 5.42 points.El valor más alto fue en Finlandia: 7.77 points y el valor más bajo fue en Rep. Centroafricana: 3.08 points.")
                ], className='row'),
            ], className='row')
        ])
    ])
])

@app.callback(
    [Output('map', 'figure'),Output('bar', 'figure')],[Input('select_var', 'value')])

def update_graph(select_var):
    
    main_var = var[select_var]
    print(main_var)
    data_bar = data[:10]

    title = 'Distribución del indice de felicadad 2019 por' + main_var

    charts = [ 
        # Choropleth map
        px.choropleth(
                data_frame=data,
                locationmode='country names',
                projection='equirectangular',
                locations=data['Country or region'],
                color=main_var,
                hover_data=['Country or region', main_var],
                color_continuous_scale=px.colors.sequential.YlOrRd,
                labels={str(main_var)},
                width= 1280,
                height=800,
                scope='world'
        ),
    # Bar chart
        px.bar(
            data_bar,
            x='Country or region', 
            y=['GDP per capita', 'Social support',	'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption'],
            title='Top 10 de los paises con mejor puntuación'
        )
    ]

    layout_map = dict(
        title = title,
        font=dict(size=14),
        
        width=1100,
        height=800,
    )

    return charts


if __name__ == '__main__':
    app.run_server(debug=True)
