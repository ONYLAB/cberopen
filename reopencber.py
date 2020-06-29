import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly

import pandas as pd
import numpy as np
from datetime import datetime

import plotly.graph_objects as go
import plotly.express as px

from scipy.interpolate import interp1d

from utils import local_daily_graph_gen, daily_graph_gen

app = dash.Dash(__name__)

# loading the local dataset
county_death_df = pd.read_csv('https://raw.githubusercontent.com/ONYLAB/cberopen/master/time_series_covid19_deaths_local.csv')
county_confirmed_df = pd.read_csv('https://raw.githubusercontent.com/ONYLAB/cberopen/master/time_series_covid19_confirmed_local.csv')
county_df = pd.read_csv('https://raw.githubusercontent.com/ONYLAB/cberopen/master/cases_county.csv')

county_death_df.fillna(0, inplace=True)
county_confirmed_df.fillna(0, inplace=True)
county_df.fillna(0, inplace=True)

# loading the dataset
death_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
country_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv')

# droping the 'Province/State' columns as it containd null values
death_df.drop('Province/State', axis=1, inplace=True)
confirmed_df.drop('Province/State', axis=1, inplace=True)
recovered_df.drop('Province/State', axis=1, inplace=True)
country_df.drop(['People_Tested', 'People_Hospitalized'], axis=1, inplace=True)

# change columns name
death_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
confirmed_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
recovered_df.rename(columns={'Country/Region': 'Country'}, inplace=True)
country_df.rename(columns={'Country_Region': 'Country', 'Long_': 'Long'}, inplace=True)

# sorting country_df with highest confirm case
country_df.sort_values('Confirmed', ascending=False, inplace=True)

# fixing the size of circle to plot in the map
margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)

# ploting world map, fixing the size of circle
margin = country_df['Confirmed'].values.tolist()
circel_range = interp1d([1, max(margin)], [0.2,12])
circle_radius = circel_range(margin)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# navbar code
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(html.A("Daily Local Data", href="#nav-local-daily-graph", style = {'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Daily Global Data", href="#nav-daily-graph", style = {'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Most effected countries", href="#nav-top-country-graph", style = {'color': '#fff'}), className="mr-5"),
        dbc.NavItem(html.A("Country comparison", href="#nav-cr-link", style = {'color': '#fff'}), className="mr-5"),
    ],
    brand="COVID-19",
    brand_href="/",
    color="dark",
    dark=True,
    className="p-3 fixed-top"
)

# main heading
main_heading = dbc.Container(
[
    html.H1(["REOPEN CBER"], className="my-5 pt-5 text-center"),
 ]
, className='pt-3')

# what is covid-19
what_is_covid = dbc.Container(
    [
        html.Div([
            html.H3('What is COVID-19?'),
            html.P("A coronavirus is a kind of common virus that causes an infection in your nose, sinuses, or upper throat. Most coronaviruses aren't dangerous."),
            html.P("COVID-19 is a disease that can cause what doctors call a respiratory tract infection. It can affect your upper respiratory tract (sinuses, nose, and throat) or lower respiratory tract (windpipe and lungs). It's caused by a coronavirus named SARS-CoV-2."),
            html.P("It spreads the same way other coronaviruses do, mainly through person-to-person contact. Infections range from mild to serious."),
            html.Span('More information about the novel coronavirus can be obtained from '),
            html.A(' here.', href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019')
#             dcc.Link(' here.', href='https://www.who.int/emergencies/diseases/novel-coronavirus-2019')
        ])
    ]
, className="mb-5")

# LOCAL TALLY
local_tally = dbc.Container(
    [
        html.H2('Local COVID-19 Data and Statistics', style = {'text-align': 'center'}),
        
        dbc.Row(
            [
                dbc.Col(children = [html.H4('Total Confirmed'), 
                        html.Div(county_df['Confirmed'].sum()-county_df.loc[county_df.County == 'AllCounties','Confirmed'].values[0], className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
#                 dbc.Col(children = [html.H4('Recovered', style = {'padding-top': '0px'}),
#                         html.Div(country_df['Recovered'].sum(), className='text-success', style = {'font-size': '34px', 'font-weight': '700'})],
#                         width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Total Death', style = {'padding-top': '0px'}), 
                        html.Div(county_df['Deaths'].sum()-county_df.loc[county_df.County == 'AllCounties','Deaths'].values[0], className='text-danger', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
#                 dbc.Col(children = [html.H4('Active'),
#                         html.Div(country_df['Active'].sum(),className='text-warning', style = {'font-size': '34px', 'font-weight': '700'})],
#                         width=3, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='my-4 shadow justify-content-center'),
            
        html.Span("According to our statistical analysis, as of June 29, 2020, 76.9% of the local employees live in a county where there is a downward trajectory of documented cases within a 14-day period as suggested by "),
        html.A(' the White House Opening up America Again Guidelines.', href='https://www.whitehouse.gov/wp-content/uploads/2020/04/Guidelines-for-Opening-Up-America-Again.pdf'),
        html.Span(" More detail on our statistical analysis and data can be obtained from this "),
        html.A(' report.', href='https://www.whitehouse.gov/wp-content/uploads/2020/04/Guidelines-for-Opening-Up-America-Again.pdf')
    ]
)

############ NEW LOCAL
# daily data heading

local_daily_graph_heading = html.H2(id='nav-local-daily-graph', children='Local Daily Data ', className='mt-5 pb-3 text-center')

# dropdown to select the county, category and number of days

daily_county = county_confirmed_df['County'].unique().tolist()
daily_county_list = []

my_df_type = ['Confirmed cases', 'Deaths']
my_df_type_list = []

for i in daily_county:
    daily_county_list.append({'label': i, 'value': i})
    
for i in my_df_type:
    my_df_type_list.append({'label': i, 'value': i})
    
# dropdown to select county
county_dropdown = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [html.Label('Select County'), 
                        html.Div(dcc.Dropdown(id = 'select-county', options = daily_county_list, value='AllCounties'))],
                        width=3, className='p-2 mr-5'),
                
                dbc.Col(children = [html.Label('Drag to choose #Days', style = {'padding-top': '0px'}),
                        html.Div(dcc.Slider( id = 'select-date-county',
                                            min=10,
                                            max=len(county_death_df.columns[3:]),
                                            step=1,
                                            value=40
                                        ,className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-5'),
                
                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}), 
                        html.Div(dcc.Dropdown(id = 'select-category-county', options = my_df_type_list, value='Confirmed cases'))],
                        width=3, className='p-2 ml-5'),
            ]
        , className='my-4 justify-content-center'),
            
    ]
)




# WORLD TALLY
world_tally = dbc.Container(
    [
        html.H2('World Data', style = {'text-align': 'center'}),
        
        dbc.Row(
            [
                dbc.Col(children = [html.H4('Confirmed'), 
                        html.Div(country_df['Confirmed'].sum(), className='text-info', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H4('Recovered', style = {'padding-top': '0px'}),
                        html.Div(country_df['Recovered'].sum(), className='text-success', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Death', style = {'padding-top': '0px'}), 
                        html.Div(country_df['Deaths'].sum(), className='text-danger', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right p-2'),
                
                dbc.Col(children = [html.H4('Active'),
                        html.Div(country_df['Active'].sum(),className='text-warning', style = {'font-size': '34px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light p-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='my-4 shadow justify-content-center'),
            
    ]
)

# global map heading
global_map_heading = html.H2(children='World map view', className='mt-5 py-4 pb-3 text-center')
# ploting the map
map_fig = px.scatter_mapbox(country_df, lat="Lat", lon="Long", hover_name="Country", hover_data=["Confirmed", "Deaths"],
                        color_discrete_sequence=["#e60039"], zoom=2, height=500, size_max=50, size=circle_radius)
map_fig.update_layout(mapbox_style="open-street-map", margin={"r":0,"t":0,"l":0,"b":0}, height=520)

# daily data heading
daily_graph_heading = html.H2(id='nav-daily-graph', children='COVID-19 daily data and Total cases ', className='mt-5 pb-3 text-center')
# dropdown to select the country, category and number of days
daily_country = confirmed_df['Country'].unique().tolist()
daily_country_list = []

my_df_type = ['Confirmed cases', 'Death rate', 'Recovered cases']
my_df_type_list = []

for i in daily_country:
    daily_country_list.append({'label': i, 'value': i})
    
for i in my_df_type:
    my_df_type_list.append({'label': i, 'value': i})
    
# dropdown to select country
country_dropdown = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [html.Label('Select Country'), 
                        html.Div(dcc.Dropdown(id = 'select-country', options = daily_country_list, value='US'))],
                        width=3, className='p-2 mr-5'),
                
                dbc.Col(children = [html.Label('Drag to choose #Days', style = {'padding-top': '0px'}),
                        html.Div(dcc.Slider( id = 'select-date',
                                            min=10,
                                            max=len(death_df.columns[3:]),
                                            step=1,
                                            value=60
                                        ,className='p-0'), className='mt-3')],
                        width=3, className='p-2 mx-5'),
                
                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}), 
                        html.Div(dcc.Dropdown(id = 'select-category', options = my_df_type_list, value='Confirmed cases'))],
                        width=3, className='p-2 ml-5'),
            ]
        , className='my-4 justify-content-center'),
            
    ]
)

# top 10 country with covid-19 heading
top_country_heading = html.H2(id='nav-top-country-graph', children='Top most Effected countries with COVID-19', className='mt-5 pb-3 text-center')
# dropdown to select no of country
no_of_country = []
top_category = country_df.loc[0:, ['Confirmed', 'Active', 'Deaths', 'Recovered', 'Mortality_Rate']].columns.tolist()
top_category_list = []

for i in range(1,180):
    no_of_country.append({'label': i, 'value': i})
    
for i in top_category:
    top_category_list.append({'label': i, 'value': i})    

# country dropdown object
top_10_country = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(children = [html.Label('Select no of Country'), 
                        html.Div(dcc.Dropdown(id = 'no-of-country', options = no_of_country, value=10))],
                        width=3, className='p-2 mr-5'),
                
                dbc.Col(children = [html.Label('Select category', style = {'padding-top': '0px'}), 
                        html.Div(dcc.Dropdown(id = 'top-category', options = top_category_list, value='Confirmed'))],
                        width=3, className='p-2 ml-5'),
            ]
        , className='my-4 justify-content-center'),
            
    ]
)

# heading 
cr_heading = html.H2(id='nav-cr-link', children='Confirmed and Recovered cases', className='mt-5 pb-3 text-center')

# confrirm and recovered cases
top_country = country_df.head(10)
top_country_name = list(top_country['Country'].values)

cr = go.Figure(data=[
    go.Bar(name='Confirmed',marker_color='#f36', x=top_country_name, y=list(top_country['Confirmed'])),
    go.Bar(name='Recovered', marker_color='#1abc9c',x=top_country_name, y=list(top_country['Recovered'])),
])

# Change the bar mode
cr.update_layout(barmode='group', height=600, title_text="Top 10 countries with Confirmed and Recovered cases")

end = html.Div(children= [
        html.H3('Sources:'),
        html.Div([html.Span('1. The global data are taken from '), html.A('Johns Hopkins University', href='https://github.com/CSSEGISandData/COVID-19')]),
        html.Div([html.Span('2. The US county-level data are taken from '), html.A('NYtimes', href='https://www.nytimes.com/interactive/2020/us/coronavirus-us-cases.html')]),    
        html.Div([html.Span('3. Build a dashboard using '), html.A('Plotly', href='https://plotly.com/')]), 
        html.Div([html.Span('4. Learn how to make simple dashboards '), html.A('here', href='https://medium.com/@benaikumar2/interactive-covid-19-dashboard-with-plotly-c0da1008b00')]),
        html.Div([html.Span('5. DMV Local Map is obtained from U.S. Census Bureau - U.S. Census Bureau, Economics and Statistics Administration, U.S. Department of Commerce.')])    
#         html.H5('Note: Will be updating this Dashboard with more features and better visualization.', style = {'margin-top': '20px', 'margin-bottom': '140px'})
])

# main layout for Dash
app.layout = html.Div(
     [navbar,
     main_heading,
     what_is_covid,      
     html.Hr(),
     local_tally,
      
      # daily report graph
      dbc.Container([local_daily_graph_heading,
                    county_dropdown,
                    html.Div(id='county-total'),
         dcc.Graph(
             id='local-daily-graphs'
         )
        ]
      ),
     
     html.Br(), 
     html.Div(html.Img(src='https://raw.githubusercontent.com/ONYLAB/cberopen/master/DMVMap.png',
              height=800),style={'text-align': 'center'}),
      
     html.Hr(), 
     world_tally,
             
     # global map           
     html.Div(children = [global_map_heading,
         dcc.Graph(
             id='global_graph',
             figure=map_fig
         )
        ]
      ),
          
      # daily report graph
      dbc.Container([daily_graph_heading,
                    country_dropdown,
                    html.Div(id='country-total'),
         dcc.Graph(
             id='daily-graphs'
         )
        ]
      ),
    
       # top countrie
      dbc.Container([top_country_heading,
                    top_10_country,
         dcc.Graph(
             id='top-country-graph'
         )
        ]
      ),
        
      # confiremd and recovered cases
      dbc.Container(children = [cr_heading,
         dcc.Graph(
             id='cr',
             figure=cr
         )
        ]
      ),
      
      # conclusion
      dbc.Container(
          end
      ),
      html.Hr()
    ]
)

# start the server
server = app.server

##################################
##################################
# CALLBACK FUNCTIONS
##################################
##################################

##################################
# call back function to make change on click
@app.callback(
     [Output('daily-graphs', 'figure')],
     [Input('select-country', 'value'),
      Input('select-category', 'value'),
      Input('select-date', 'value')]
)
def country_wise(country_name, df_type, number):
    # on select of category copy the dataframe to group by country
    if df_type == 'Confirmed cases':
        df_type = confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'
        
    elif df_type == 'Death rate':
        df_type = death_df.copy(deep=True)
        category = 'COVID-19 Death rate'
        
    else:
        df_type = recovered_df.copy(deep=True)
        category = 'COVID-19 recovered cases'
        
    
    # group by country name
    country = df_type.groupby('Country')
    
    # select the given country
    country = country.get_group(country_name)
    
    # store daily death rate along with the date
    daily_cases = []
    case_date = []
    
    # iterate over each row
    for i, cols in enumerate(country):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(country[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)
            
            # creata a data frame
            new_df = pd.DataFrame(data = zip_all_list, columns=['Date','coronavirus'])

    # append the country to the data frame
    new_df['Country'] = country['Country'].values[0]
    
    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) -1):
        new_df.iloc[i+1, 1] = new_df.iloc[1+i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i+1, 1] < 0:
            new_df.iloc[i+1, 1] = 0
    
    new_df = new_df.iloc[-number:]
    
    return (daily_graph_gen(new_df, category))
##################################

##################################
# show total data for each country
@app.callback(
     [Output('country-total', 'children')],
     [Input('select-country', 'value')]
)
def total_of_country(country):
#     country = new_df['Country'].values[0]
    
    # get the country data from country_df
    my_country = country_df[country_df['Country'] == country].loc[:, ['Confirmed', 'Deaths', 'Recovered', 'Active']]
    
    country_total = dbc.Container(
    [   
        html.H4('Total case count in '+ country+ ''),
        dbc.Row(
            [
                dbc.Col(children = [html.H6('Confirmed'), 
                        html.Div(my_country['Confirmed'].sum(), className='text-info', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H6('Recovered', style = {'padding-top': '0px'}),
                        html.Div(my_country['Recovered'].sum(), className='text-success', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2'),
                
                dbc.Col(children = [html.H6('Death', style = {'padding-top': '0px'}), 
                        html.Div(my_country['Deaths'].sum(), className='text-danger', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2'),
                
                dbc.Col(children = [html.H6('Active'),
                        html.Div(my_country['Active'].sum(),className='text-warning', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light pt-2', style = {'border-top-right-radius': '6px', 'border-bottom-right-radius': '6px'}),
            ]
        , className='mt-1 justify-content-center'),
            
    ]
)
    
    return [country_total]
##################################

##################################
# method to get the top countries
@app.callback(
     [Output('top-country-graph', 'figure')],
     [Input('no-of-country', 'value'),
      Input('top-category', 'value')]
    )
def top_ten(number, sort_by):
    # sorting the columns with top death rate
    country_df2 = country_df.sort_values(by=sort_by, ascending=False)
    
    # sort country with highest number of cases
    country_df2 = country_df2.head(number)
    
    top_country_data = []
    top_country_data.append(go.Bar(x=country_df2['Country'], y=country_df2[sort_by]))
    
    layout = {
        'title': 'Top ' + str(number) +' Country - ' + sort_by + ' case',
        'title_font_size': 26,
        'height':500,
        'xaxis': dict(title = 'Countries'),
        'yaxis': dict(title = sort_by)
    }
    
    figure = [{
        'data': top_country_data,
        'layout': layout
    }]
    
    return figure
##################################

##################################
# call back function to make change on click
@app.callback(
     [Output('local-daily-graphs', 'figure')],
     [Input('select-county', 'value'),
      Input('select-category-county', 'value'),
      Input('select-date-county', 'value')]
)
def county_wise(county_name, df_type, number):
    # on select of category copy the dataframe to group by county
    if df_type == 'Confirmed cases':
        df_type = county_confirmed_df.copy(deep=True)
        category = 'COVID-19 confirmed cases'
        
    elif df_type == 'Deaths':
        df_type = county_death_df.copy(deep=True)
        category = 'COVID-19 Death'        
    
    # group by county name
    county = df_type.groupby('County')
    
    # select the given county
    county = county.get_group(county_name)
    
    # store daily death rate along with the date
    daily_cases = []
    case_date = []
    
    # iterate over each row
    for i, cols in enumerate(county):
        if i > 3:
            # take the sum of each column if there are multiple columns
            daily_cases.append(county[cols].sum())
            case_date.append(cols)
            zip_all_list = zip(case_date, daily_cases)
            
            # creata a data frame
            new_df = pd.DataFrame(data = zip_all_list, columns=['Date','coronavirus'])

    # append the county to the data frame
    new_df['County'] = county['County'].values[0]
    
    # get the daily death rate
    new_df2 = new_df.copy(deep=True)
    for i in range(len(new_df) -1):
        new_df.iloc[i+1, 1] = new_df.iloc[1+i, 1] - new_df2.iloc[i, 1]
        if new_df.iloc[i+1, 1] < 0:
            new_df.iloc[i+1, 1] = 0
    
    new_df = new_df.iloc[-number:]
    
    return (local_daily_graph_gen(new_df, category))
##################################

##################################
# show total data for each county
@app.callback(
     [Output('county-total', 'children')],
     [Input('select-county', 'value')]
)
def total_of_county(county):
#     county = new_df['County'].values[0]
    
    # get the county data from county_df
    my_county = county_df[county_df['County'] == county].loc[:, ['Confirmed', 'Deaths']]
    
    county_total = dbc.Container(
    [   
        html.H4('Total case count in '+ county+ ''),
        dbc.Row(
            [
                dbc.Col(children = [html.H6('Confirmed'), 
                        html.Div(my_county['Confirmed'].sum(), className='text-info', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2', style = {'border-top-left-radius': '6px', 'border-bottom-left-radius': '6px'}),
                
                dbc.Col(children = [html.H6('Death', style = {'padding-top': '0px'}), 
                        html.Div(my_county['Deaths'].sum(), className='text-danger', style = {'font-size': '28px', 'font-weight': '700'})],
                        width=3, className='text-center bg-light border-right pt-2')
            ]
        , className='mt-1 justify-content-center'),
            
    ]
)
    
    return [county_total]
##################################

##################################
# RUN SERVER
##################################
if __name__ == '__main__':
    app.run_server()