# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        pie_chart = spacex_df[["Launch Site", "class"]].groupby(by="Launch Site").sum().reset_index()
        fig = px.pie(pie_chart, values='class', 
             names="Launch Site",
             title='Launch Site Success Rate')
    else:
        pie_chart = spacex_df[spacex_df["Launch Site"] == entered_site][["Launch Site", "class"]].groupby(by="class").count().reset_index()
        fig = px.pie(pie_chart, values='Launch Site', 
             names="class",
             title=f'{entered_site} Launch Success Rate')
    return fig

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={
            'textAlign': 'center',
            'color': '#503D36',
            'font-size': 40
        }
    ),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
        ],
        value='ALL',
        placeholder="Select Launch Site Here",
        searchable=True
    ),
    
    html.Br(),

    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=500,
                    marks={0: '0', 10000: '10000'}, value=[min_payload, max_payload]),

    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
               Input(component_id='payload-slider', component_property='value')])
def get_scatter_plot(site, payload):
    min_value, max_value = payload

    filtered_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= min_value) & (spacex_df["Payload Mass (kg)"] <= max_value)]

    if site != 'ALL':
        filtered_df = filtered_df[filtered_df["Launch Site"] == site]

    fig = px.scatter(
        filtered_df,        # DataFrame containing your data
        x='Payload Mass (kg)',  # Column to plot on the x-axis
        y='class',  # Column to plot on the y-axis
        color='Booster Version Category',
        title=f'{site} Scatter Plot Payload vs. Success'
    )

    return fig
    

# Run the app
if __name__ == '__main__':
    app.run_server()
