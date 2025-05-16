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

# Create list of launch sites
launch_sites = spacex_df['Launch Site'].unique().tolist()
drop_down_options_lst = [{'label': 'All Sites', 'value': 'ALL'}]

for site in launch_sites:
    drop_down_options_lst.append({'label': site, 'value': site})


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=drop_down_options_lst,
                                             value='ALL',
                                             placeholder="Place holder here",
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
                                                mi=0,
                                                max=10000,
                                                step=1000,
                                                marks={a: str(a) for a in range(0, 11000, 1000)},
                                                value=[spacex_df["Payload Mass (kg)"].min().item(),
                                                       spacex_df["Payload Mass (kg)"].max().item()]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output


@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):

    if entered_site == 'ALL':
        title = "Success launch rate for all spacex launches"
        filtered_df = spacex_df
        unique_sites = spacex_df['Launch Site'].unique().tolist()
        suc_lst = []

        for usite in unique_sites:
            suc_lst.append(filtered_df.loc[filtered_df['Launch Site'] == usite, 'class'].sum().item())


        df3 = pd.DataFrame(list(zip(unique_sites, suc_lst)), columns=['Sites', 'Success'])
        fig = px.pie(df3, names='Sites', values='Success', title=title)


    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        title = f'Success launch rate for {entered_site}'
        total = filtered_df.shape[0]
        success = filtered_df['class'].sum().item()
        fig = px.pie(names=['Success', 'Failure'], values=[success, total-success],
                     title=title)
    # Return outcomes piechart for a a selected site


    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")]
)
def get_scatter_plot(entered_site, entered_payload):

    if entered_site == 'ALL':
        filtered_df = spacex_df
        fig = px.scatter(filtered_df,
                         x="Payload Mass (kg)",
                         y='class',
                         color="Booster Version Category",
                         title="Outcomes for all spacex sites")
        pass
    else:
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.scatter(filtered_df,
                         x="Payload Mass (kg)",
                         y='class',
                         color="Booster Version Category",
                         title=f"Outcomes for {entered_site}")


    return fig


# Run the app
if __name__ == '__main__':
    app.run()
