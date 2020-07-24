import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

# images

image_filename = 'data/happy.png' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

# import and work on data
data = pd.read_csv(r"data/World_Happinnes.csv")

var = {1: 'Score', 2: 'GDP per capita', 3: 'Social support', 4: 'Freedom to make life choice',
       5: 'Generosity', 6: 'Perceptions of corruption'}
df = data.groupby(['Country or region', 'Score'])

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
                html.Img(src='data:image/png;base64,{}'.format(encoded_image)),
                html.Div([
                    dcc.Graph(id='bar'),
                    html.P("El índice global de felicidad es una publicación anual de las Naciones Unidas que mide la felicidad en 157 países, basándose en diversos factores, como el PIB per cápita," +
                           "la esperanza de vida saludable y el apoyo social, la primera que que se realizo el estudio fue en el 2012"),
                ], className='two columns'),
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
    df = create_data(select_var)


    choropleth = [ dict(
        type= 'choropleth',
        z=df,
        locationmode= 'ISO-3',
        zmin= 0.,
        zmax=10.,
        colorscale=00,
        showscale=True,
        colorbar = dict(
            autotick=False,
        ),
        font=dict(size=12),
        hovertemplete = "",
    )]

    layout_dict = dict(
        title = "",
        font=dict(size=14),
        
        width=1100,
        height=800,
    )

    return {

    }


def create_data(var):
    pass


if __name__ == '__main__':
    app.run_server(debug=True)
