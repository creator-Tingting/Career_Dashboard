from dash import Dash, html, dcc, callback, Output, Input
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def charts_div(job):
    linkin_data = pd.read_csv('data/linkin.csv')
    linkin_data["longitude"] = pd.to_numeric(linkin_data["longitude"])
    linkin_data["latitude"] = pd.to_numeric(linkin_data["latitude"])

    # Filter data for "Where they studied" and specific job title
    map_df = linkin_data[(linkin_data["Category"] == "Where they studied") & (linkin_data["Title"] == job)].dropna()

    # Generate heatmap using percentage of each location
    fig_map = where_they_studied(map_df)

    # Data for "What they studied"
    jobs_df = linkin_data[(linkin_data["Title"] == job) & (linkin_data["Category"] == "What they studied")]
    jobs_df = jobs_df.groupby('Location').aggregate({"Value": "sum"}).reset_index().sort_values(by='Value', ascending=False)

    # Generate the bar chart (only top 10 based on percentage)
    fig = what_studied(jobs_df)

    # Filter data for "What they are skilled at" and specific job title
    skilled_df = linkin_data[(linkin_data["Category"] == "What they are skilled at") & (linkin_data["Title"] == job)]
    skilled_df = skilled_df.groupby('Location').aggregate({"Value": "sum"}).reset_index().sort_values(by='Value', ascending=False)

    # Generate treemap using percentage of each skill (only top 10)
    skilled_fig = what_skilled_at(skilled_df)

    # Layout style
    item_style = {"background-color":  "#e6e6fc",
                  "height": "100%",
                  "border-radius": "10px",
                  "box-shadow": "5px 5px 15px rgba(0, 0, 0, 0.3)",
                  "margin": "10px",
                  "display": "grid",
                  "align-items": "center",
                  "justify-items": "center",
                  "text-align": "center",
                  "padding": '5px'}

    return html.Div(style={
        'display': "grid",
        "grid-template-columns": "repeat(3,1fr)",
        "grid-gap": "10px",
        "height": "50vh",
        "justify-item": "center",
        "margin": "10px 0px 0px 0px",
        "background-color": "#eef5fe"
    },
        children=[
        dcc.Graph(id='example-graph_map', figure=fig_map, style=item_style),
        dcc.Graph(id='example-graph', figure=fig, style=item_style),
        dcc.Graph(id='example-graph_skilled', figure=skilled_fig, style=item_style)
    ])


# Updated `where_they_studied` function
def where_they_studied(df):
    # Group by Location, latitude, and longitude, and sum the Value for each location
    location_counts = df.groupby(['Location', 'latitude', 'longitude'])['Value'].sum().reset_index(name='TotalValue')
    total_value = location_counts['TotalValue'].sum()
    location_counts['Percentage'] = (location_counts['TotalValue'] / total_value) * 100

    # Select only top 10 locations with the highest percentages
    location_counts_top10 = location_counts.sort_values(by='Percentage', ascending=False).head(10)
    location_counts_top10['Text'] = location_counts_top10['Location'] + ' (' + location_counts_top10['Percentage'].round(2).astype(str) + '%)'

    fig = go.Figure(go.Densitymap(
        lat=location_counts_top10["latitude"],
        lon=location_counts_top10["longitude"],
        z=location_counts_top10['Percentage'],
        radius=15,
        text=location_counts_top10["Text"], 
        hovertemplate='<b>%{text}</b><extra></extra>'
    ))

    fig.update_layout(
        title={'text': 'TOP 10 Graduate Universities (%)', 'x': 0.5, 'y': 1,
               'xanchor': 'center', 'font': {'size': 26, 'color': '#E1AC00', 'family': 'Arial', 'weight': 'bold'}},
        map=dict(style="open-street-map", center=dict(lat=-25.2744, lon=133.7751), zoom=2.5),
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


# Updated `what_studied` function
def what_studied(df):
    total_value = df['Value'].sum()
    df['Percentage'] = (df['Value'] / total_value) * 100

    # Display only top 10 locations with highest percentages
    top10_jobs_df = df.sort_values(by='Percentage', ascending=False).head(10)

    fig = px.bar(top10_jobs_df, y='Location', x='Percentage',
                 color_discrete_sequence=["#5d5799"],
                 title='TOP 10 Majors (%)', height=500, width=500)

    fig.update_traces(text=top10_jobs_df['Percentage'].round(2).astype(str) + '%', textposition='inside', textfont=dict(color='white'))

    fig.update_layout(
        title={'text': 'TOP 10 Majors (%)', 'font': {'size': 26, 'color': '#E1AC00', 'family': 'Arial', 'weight': 'bold'}, 'x': 0.5, 'xanchor': 'center'},
        xaxis_title="Percentage (%)",
        yaxis_autorange='reversed',
        margin={"r": 0, "t": 40, "l": 0, "b": 0},
        yaxis_title=None,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig


# Updated `what_skilled_at` function
def what_skilled_at(df):
    total_value = df['Value'].sum()
    df['Percentage'] = (df['Value'] / total_value) * 100

    # Display only top 10 skills with the highest percentages
    top10_skilled_df = df.sort_values(by='Percentage', ascending=False).head(10)

    fig = px.treemap(top10_skilled_df, path=[px.Constant(" "), 'Location'], values='Percentage',
                     title='TOP 10 Skills (%)',
                     color='Percentage',
                     color_continuous_scale=px.colors.sequential.Purples,
                     height=500, width=500)

    fig.update_traces(root_color="lightgrey", texttemplate='%{label}<br>%{value:.2f}%', textposition="middle center",
                      textfont_size=20, hovertemplate='%{label}<br>Percentage: %{value:.2f}%<extra></extra>')

    fig.update_layout(coloraxis_colorbar=dict(title='%', ticksuffix='%'),
                      title={'text': 'TOP 10 Skills (%)', 'font': {'size': 26, 'color': '#E1AC00', 'family': 'Arial', 'weight': 'bold'}, 'x': 0.5, 'xanchor': 'center'},
                      margin={"r": 0, "t": 40, "l": 0, "b": 0}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig
