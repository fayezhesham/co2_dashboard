import pandas as pd



df=pd.read_csv('manipulated.csv')


df=df.rename(columns={'value':'amount'})





import plotly.express as px
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc



app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([
	dbc.Row([
		dbc.Col([
			html.H4('CO2 intensity due to electricity generation in the EU 1990-2017'),
			html.P('''A set of data cllected from the EEU showing the intensity of carbon
			 dioxide emissions due to the electricity production from the year 1990 to the year 2017, All numbers are measured in (gCO2/KWh)''', id='the_text'),
		], id='title', width={'size':11, 'offset':0}),
		dbc.Col([
			html.Img(src=app.get_asset_url('image.png'), height=80, id='the_image',
			),
		], id='image', width={'size':1, 'offset':0}),
	],id='header'),

	dbc.Row([
		dbc.Col([
			html.P('select a range of years', id='slider_text'), 

			dcc.RangeSlider(
            id='range_slider', 
            marks={
                1990: '1990',     
                1995: '1995',
                2000: '2000',
                2005: '2005',
                2010: '2010',
                2015: '2015',
                2017: '2017',
            },
            step=1, 
            min=1990,
            max=2017,
            dots=True,
            updatemode='mouseup',
			value=[2000, 2005]
            ),
		], id='slider_column')
	], id='slider_container'), 

	dbc.Row([
		dbc.Col(
			dcc.Graph(id='the_graph'),
        xs=12, sm=12, md=12, lg=6, xl=6,
        id='top_left_col',
		), 
		dbc.Col(
			dcc.Graph(id='the_graph1'), 
            xs=12, sm=12, md=12, lg=6, xl=6,
            id='top_right_col',
		),
	]),

    dbc.Row([
		dbc.Col([
			html.P('select from the countries below', id='dropdown_text'), 

            dcc.Dropdown(id='dropdown',
            options=[
                {'label':x, 'value':x} for x in df.sort_values('country')['country'].unique()
                
            ],
            value=['Finland', 'Germany', 'Cyprus'],
            multi=True,
            clearable=False, )
		], id='dropdown_column')
	], id='dropdown_container'),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='line_chart')
        ], id='bottom_col', width={'size':12, 'offset':0})
    ], id='bottom_row'),

])

@app.callback(
    Output('the_graph','figure'),
    [Input('range_slider','value')]
)

def update_graph(years_chosen):

    dff=df[(df['year']>=years_chosen[0])&(df['year']<=years_chosen[1])]
    dff=dff.groupby(["country"], as_index=False)["amount"].mean()

    the_bar = px.bar(
        data_frame=dff,
        x="country",
        y="amount",
		template='plotly_dark'
    )


    return (the_bar)

@app.callback(
    Output('the_graph1','figure'),
    [Input('range_slider','value')]
)

def update_graph(years_chosen):
    ddff=df[(df['year']>=years_chosen[0])&(df['year']<=years_chosen[1])]
    dfdf=ddff.groupby(["country", 'iso_codes'], as_index=False)["amount"].mean()

    the_map = px.choropleth(dfdf, color='amount', hover_name='country', hover_data=['amount'],
							 template='plotly_dark', scope='europe', locations='iso_codes',
							  basemap_visible=True, title='Zoom into the map or click on a country', )


    return (the_map)


@app.callback(
    Output('line_chart','figure'),
    [Input('dropdown','value')]
)

def build_graph(country_chosen):
    dfs=df[df['country'].isin(country_chosen)]
    

    line_chart = px.line(dfs, x="year", y="amount", color='country',template='plotly_dark', title='Change overtime')
    
    return line_chart


if __name__ == "__main__":
   app.run_server(host='0.0.0.0', port=8050, debug=False)

