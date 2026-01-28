from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import warnings

item_style = {
    "background-color": "#e6e6fc",  # card color
    "height": "100%",
    "border-radius": "10px",
    "box-shadow": "5px 5px 15px rgba(0, 0, 0, 0.3)",
    "margin": "10px",
    "display": "grid",
    "align-items": "center",
    "justify-items": "center",
    "text-align": "center",
    "padding": '5px'
}

def format_stars(rating):
    # Separate integer and fractional parts
    integer_part, decimal_part = divmod(float(rating), 1)
    integer_part = int(integer_part)

    # Determine stars based on decimal part
    if 0 < decimal_part < 0.5:
        return '⭐' * integer_part  # no Half star
    elif 0.5 <=decimal_part < 1:
        return f"{'⭐' * integer_part}☆"  # Half star
    else:
        return '⭐' * integer_part  # No half star

def company_info_div(job, sortby):
    companies = pd.read_csv('data/glass_data.csv')
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", pd.errors.SettingWithCopyWarning)
        companies_by_job = companies[companies['job_title'] == job]
        
        # Extract number
        try:
            companies_by_job[sortby] = companies_by_job[sortby].astype(str)
            companies_by_job[f"{sortby}_num"] = companies_by_job[sortby].str.extract(
                r'([-+]?\d*\.\d+|\d+)', expand=False)
            companies_by_job[f"{sortby}_num"] = companies_by_job[f"{sortby}_num"].fillna(0).astype(float)
            companies_by_job = companies_by_job.sort_values(
                by=f"{sortby}_num", ascending=False)
        except Exception as e:
            print(e)

    # Return the layout with title and cards
    return html.Div([

        # Title Section
        html.Div(
            html.H1(
                f"Top 10 Companies sorted by {sortby}",
                style={"text-align": "center", "color": "#E1AC00", "font-size": "32px", "font-weight": "bold"}
            ),
            style={"padding": "10px 0"}
        ),
        
        # Company Cards Section without additional border
        html.Div(
            style={
                "display": "grid",
                "grid-template-columns": "repeat(5,1fr)",
                "grid-row-gap": "20px"
            },
            children=[
                html.Div(
                    style=item_style,
                    children=[
                        html.A(
                            style={'textDecoration': 'none'},
                            children=html.Div(
                                style={"color": "#404040", 'textDecoration': 'none'},
                                children=[
                                    html.Div(
                                        style={"display": "grid", "grid-template-columns": "80px 1fr", "grid-gap": "10px"},
                                        children=[
                                            html.Img(src=company.logo, width="80px", height="80px"),
                                            html.Div(
                                                style={"text-align": "left", "font-size": "24px"},
                                                children=[
                                                    html.Div(children=[f"{company.Cards_titles}"]),
                                                    html.Div(
                                                        style={"font-size": "20px"},
                                                        children=[
                                                            f"{company.Ratings}",
                                                            format_stars(company.Ratings)  # Use formatted stars
                                                        ]
                                                    ),
                                                ]
                                            )
                                        ]
                                    ),
                                    html.Div(
                                        style={"display": "grid", "grid-template-columns": "1fr 1fr 1fr", "margin-top": "5px"},
                                        children=[
                                            html.Div(children=[
                                                html.Div(children=f"{company.Salaries}"),
                                                html.Div(children="Salaries"),
                                            ]),
                                            html.Div(children=[
                                                html.Div(children=f"{company.Reviews}"),
                                                html.Div(children="Reviews"),
                                            ]),
                                            html.Div(children=[
                                                html.Div(children=f"{company.Jobs_count}"),
                                                html.Div(children="Jobs Count"),
                                            ]),
                                        ]
                                    )
                                ]
                            ),
                            href=company.url, target="_blank"
                        ),
                    ]
                ) for company in companies_by_job.itertuples()
            ]
        )
    ])
