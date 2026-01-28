from dash import Dash, html, dcc, callback, Output, Input
from .job_info import get_job_infos
from .company_info import company_info_div
from .charts_area import charts_div
import pandas as pd

countries = ['Australia']
company_size = pd.read_csv('data/glass_data.csv')
sort_company_by = ["Salaries", "Ratings","Job Counts"]

jobs=["Data Analyst",
"Software Engineer",
"Mining Engineer",
"Lawyer",
"Accountant",
"Banker",
"Electrical Engineer",
"Sales Manager",
"Nurse",
"General Practitioner"]


def search_area():
    return html.Div(style={
        'display': "grid",
        "background-color": "#eef5fe",  #change color here
        "grid-template-rows": "200px,20vh,30vh,80vh",
        'height': "140vh",
        "border": "1px solid black",
        "margin": "10px 0px",
        "justify-item": "center",
        "grid-row-gap": "10px"
    },
        children=[
            html.Div(
                style={"display": 'grid', "font-size": 24,
                       "grid-template-columns": "repeat(3,1fr)", "grid-gap": "10px"},
                children=[
                    html.Div(children=[html.Label(" 💼"+ ' Select a Job:',style={"color": "#3f007d", "font-weight": "bold"}),
                                       dcc.Dropdown(jobs,  jobs[0], id='search_job')],),
                     html.Div(children=[html.Label(" 📍"+ ' Select a Country:',style={"color": "#3f007d", "font-weight": "bold"}),
                                       dcc.Dropdown(countries,  countries[0], id='search_country')]),
                      html.Div(children=[html.Label(" 🔍"+ ' Ranked by:',style={"color": "#3f007d", "font-weight": "bold"}),
                                       dcc.Dropdown(sort_company_by,  sort_company_by[0], id='sort_company_by')]),
                 
                ]),
            html.Div(id='job_info_output'),
            html.Div(id='company_info_output'),
            html.Div(id='charts_area_output'),
    ])



@callback(
    Output(component_id='job_info_output', component_property='children'),
    Input(component_id='search_job', component_property='value')
)
def update_part1(value):
    if value:
        return get_job_infos(value)
    else:
        return ''



@callback(
    Output(component_id='company_info_output', component_property='children'),

    [Input(component_id='search_job', component_property='value'),
     Input(component_id='sort_company_by', component_property='value')]
)
def update_part2(job, sortBy):
    if job:
        return company_info_div(job, sortBy)



@callback(
    Output(component_id='charts_area_output', component_property='children'),
    Input(component_id='search_job', component_property='value')
)
def update_part4(value):
    if value:
        return charts_div(value)
