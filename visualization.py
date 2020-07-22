import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import dash 
import dash_core_components as components
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)


# import and work on data
data = pd.read_csv(r"data/World_Happinnes.csv") 

var = {1:'Score', 2: 'GDP per capita', 3: 'Social support', 4: 'Freedom to make life choice',
        5: 'Generosity', 6: 'Perceptions of corruption'}
df = data.groupby(['rank', 'Score','Country or region', 'GDP per capita', 'Social support', 'Freedom to make life choices','Generosity','Perceptions of corruption',])


 # App layout
app.layout = html.Div([
    
    html.H1("Indice de Felicidad 2019", style={'text-align': 'left', 'color':'blue'}),
    
    components.Dropdown(id="select_var",
             options=[
                 {"label":"Score", "value": 1},
                 {"label": "GDP per capita", "value": 2},
                 {"label": "Social support", "value": 3},
                 {"label": "Freedom to make life choices", "value": 4},
                 {"label": "Generosity", "value": 5},
                 {"label": "Perceptions of corruption", "value":6}],
             multi=False,
             value=1,
             style={'width': "40%"}
             ),

    html.Div(id = 'container', children=[]),
    html.Br(),

    components.Graph(id='choropleth',figure={}),

    html.H1("Indice de Felicidad", style={'text-align': 'center', 'color': 'blue'}),

    html.P("El índice global de felicidad es una publicación anual de las Naciones Unidas que mide la felicidad en 157 países, basándose en diversos factores, como el PIB per cápita,"+
    "la esperanza de vida saludable y el apoyo social, la primera que que se realizo el estudio fue en el 2012"),
    
    html.P("El promedio para 2019 fue de 5.42 points.El valor más alto fue en Finlandia: 7.77 points y el valor más bajo fue en Rep. Centroafricana: 3.08 points.")

    components.Graph(id= 'bar_chart', figure={}),
])


@app.callback(
    [Output(component_id='container', component_property='children'),
    Output(component_id='choropleth',component_property='figure'),
    Output(component_id='bar_chart', component_property='figure')],
    [Input(component_id='select_var', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    option = var[1]

    map = go.Figure(
        data = [go.Choropleth(
            locationmode='ISO-3',
            locations=df["Country or region"],
            z=data[option].astype(float),
            colorscale='YlGnBu',
        )]
    )

    map.update_layout(
        title_text='Word Happinnes by {}'.format(option),
        title_xanchor="center",
        title_font=dict(size=24),
        title_x=0.5,
        geo=dict(scope='ISO-3'),
    )
    
    bar = px.bar(df,x='Country or region', y='Score', orientation='h')

    return map, bar

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)