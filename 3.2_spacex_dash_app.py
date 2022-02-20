# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

#list options for drop down
options_list = [{'label': 'All Sites', 'value': 'ALL'}]
for site in spacex_df['Launch Site'].unique():
    options_list.append({'label': site, 'value': site})
# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                  dcc.Dropdown(id='site-dropdown',
                                    options=options_list,
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                    ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0,
                                                max=10000,
                                                step=1000,
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    # check if df needs to be filtered by site
    if entered_site == 'ALL':
        fig = px.pie(spacex_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site')
        return fig
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
        counts = data['class'].value_counts()
        fig = px.pie(data,
            values=counts,
            names=counts.index,
            title='Total Success Launches for site {}'.format(entered_site),
            color=counts.index,
            color_discrete_map = {0: 'red', 1: '#5bef67'})
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
            [Input(component_id='site-dropdown', component_property='value'),
            Input(component_id="payload-slider", component_property="value")]
            )
def get_scatter_chart(entered_site, payload_range):
    # check if all sites or one site
    if entered_site == 'ALL':
        data = spacex_df
    else:
        data = spacex_df[spacex_df['Launch Site'] == entered_site]
    # filter df for payload mass range
    data = data[(payload_range[0] <= data['Payload Mass (kg)']) & (data['Payload Mass (kg)'] <= payload_range[1])]
    # build scatter chart
    fig = px.scatter(data_frame=data,
                    x='Payload Mass (kg)',
                    y='class',
                    color='Booster Version Category',
                    title=f'Correlation between Payload and Success for site {entered_site}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
