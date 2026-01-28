from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

replacement_dict = {
    "job": "Job Opportunities",
    "salary": "Salary",
    "growth": "Growth",
    "star": "Job Satisfaction"
}
bgc = "#5d5799"
def get_content_job(job_row, col):
    return html.Div(children=[
        html.Div(style={"font-size": 30, "color": "#fdca17"}, children="💡 "+  replacement_dict[col]),
        html.Div(style={"font-size": 48, "color": "white"}, children=f"{job_row[col]}")
    ])

def get_content_salary(job_row, col):
    return html.Div(children=[
        html.Div(style={"font-size": 30, "color": "#fdca17"},   children="💰"+ replacement_dict[col]),
        html.Div(style={"font-size": 48, "color": "white"}, children=f"{job_row[col]}"),
        html.Div(style={"font-size": 24, "color": "white"}, children="Typical annual salary in Australia")
    ])

def get_content_growth(job_row, col):
    return html.Div(children=[
        html.Div(style={"font-size": 30, "color": "#ffc008"},   children="⚡️ "+ replacement_dict[col]),
        html.Div(style={"font-size": 48, "color": "white"}, children=f"{job_row[col]}"),
        html.Div(style={"font-size": 24, "color": "white"}, children="5-year projection")
    ])

def get_content_star(job_row, col):
    return html.Div(children=[
        html.Div(style={"font-size": 30, "color": "#fdca17"},   children="💗"+ replacement_dict[col]),
        html.Div(style={"font-size": 48, "color": "white"}, children=f"{str(job_row[col])}"),
        html.Div(style={"font-size": 16, "color": "white"}, children=f"{'⭐'* int(job_row[col])}")
    ])


def get_job_infos(job):
    seek_infos = pd.read_csv('data/seek.csv')
    job_row = seek_infos[seek_infos['search_title'] == job].iloc[0]
    item_style = {"background-color": bgc,
                  "height": "100%",
                  "border-radius": "10px",
                  "box-shadow": "5px 5px 15px rgba(0, 0, 0, 0.3)",
                  "margin": "10px",
                  "display": "grid",
                  "align-items": "center",
                  "justify-items": "center",
                  "text-align": "center",
                  }
    return html.Div(style={
        "margin-top": "10px",
        "width": "100%",
        "height": "150px",
        "display": "grid",
        "grid-template-columns": "1fr 1fr 1fr 1fr",
        "align-items": "center",
        "justify-content": "center",
        "transition": "box-shadow 0.3s ease",
    }, children=[
        html.Div(style=item_style, children=get_content_job(job_row, 'job')),
        html.Div(style=item_style,
                 children=get_content_salary(job_row, 'salary')),
        html.Div(style=item_style,
                 children=get_content_growth(job_row, 'growth')),
        html.Div(style=item_style, children=get_content_star(job_row, 'star'))
    ])
