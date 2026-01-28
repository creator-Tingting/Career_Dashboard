from dash import Dash, html, dcc, callback, Output, Input,State
import dash
import os
import dash_bootstrap_components as dbc
from openai import OpenAI
from components.search_area import search_area

"""In this project, we utilized pandas for data processing, plotly and Dash for interactive visualization and web application development,
dash_bootstrap_components for styling, warnings for managing runtime warnings, os for file operations, openai for natural language query 
support. The detail version is specified in requirements.txt"""

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
 
app.layout = html.Div(
    style={"background-color": "#eef5fe", "box-size": "content"},
    children=[
        # Centered Title in a separate row
        html.Div(
            html.H1(
                "One-Stop Career Exploration Dashboard",
                style={'margin': '0', 'color': '#5d5799', 'text-align': 'center', 'font-weight': 'bold'}
            ),
            style={"padding": "10px 0", "background-color": "#eef5fe"}
        ),

        # Right-aligned Chatbox button and Dropdown
        html.Div(
            style={
                "display": "flex",
                "justify-content": "flex-end",  # Align buttons on the right side
                "align-items": "center",
                "padding": "10px 20px",
                "background-color": "#eef5fe",
                "gap": "10px",  # Adds spacing between chat button and dropdown
            },
            children=[
                # Chatbox button
                dbc.Button("🤖 Your Career Coach", id="open-chat-btn", n_clicks=0, 
                           style={"background-color": "#ffc008", "color": "white", "border": "none", "box-shadow": "none"}),

                # Dropdown with multiple download options
                dbc.DropdownMenu(
                    [
                        dbc.DropdownMenuItem("Download Job Market Overview Data", id="download-btn_seek"),
                        dbc.DropdownMenuItem("Download Company Profiles Data", id="download-btn_glass"),
                        dbc.DropdownMenuItem("Download Education and Skills Data", id="download-btn_linkin"),
                    ],
                    label="↓ Download",
                    group=True,
                    style={"color": "#1e50a2"},
                ),
            ],
        ),
        
        # Rest of the layout remains unchanged
        search_area(),
        dcc.Download(id="download-link_seek"),
        dcc.Download(id="download-link_glass"),
        dcc.Download(id="download-link_linkin"),

        # Off-canvas chat box (pop-out effect)
        dbc.Offcanvas(
            [
                html.H5("Chat History", className="offcanvas-title"),
                html.Div(
                    id="chat-container",
                    children=[
                        dcc.Textarea(
                            id="chat-history",
                            value='',
                            style={'width': '100%', 'height': '500px'},
                            readOnly=True
                        ),
                        dcc.Input(
                            id='user-input',
                            type='text',
                            placeholder='Message with your career coach...',
                            style={'width': '80%'}
                        ),
                        dbc.Button('Send', id='send-button', n_clicks=0, className="mt-2"),
                    ],
                ),
            ],
            id="chat-box",
            title="Your Career Coach",
            is_open=False,
            placement="end",  # Pop-out from the right side
            style={"width": "500px"},
        ),
    ]
)

# download function and callback
@app.callback(
    Output("download-link_seek", "data"),
    Input("download-btn_seek", "n_clicks"),
    prevent_initial_call=True,
)
def download_csv(n_clicks):
    file_path = os.path.join(os.getcwd(), "data/seek.csv")  # Replace with your file path
    return dcc.send_file(file_path)

@app.callback(
    dash.dependencies.Output('download-link_glass', 'data'),
    dash.dependencies.Input('download-btn_glass', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    file_path = os.path.join(
        os.getcwd(), 'data/glass_data.csv') 
    return dcc.send_file(file_path)


@app.callback(
    dash.dependencies.Output('download-link_linkin', 'data'),
    dash.dependencies.Input('download-btn_linkin', 'n_clicks'),
    prevent_initial_call=True
)
def download_csv(n_clicks):
    file_path = os.path.join(os.getcwd(), 'data/linkin.csv') 
    return dcc.send_file(file_path)

# Chatbox function and callback
@app.callback(
    Output("chat-box", "is_open"),
    Input("open-chat-btn", "n_clicks"),
    State("chat-box", "is_open"),
)
def toggle_chat(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open

# Callback to handle chat messages and interact with OpenAI API
@app.callback(
    Output('chat-history', 'value', allow_duplicate=True),
    Input('send-button', 'n_clicks'),
    State('user-input', 'value'),
    State('chat-history', 'value'),
    prevent_initial_call=True,
)
def update_chat(n_clicks, user_input, chat_history):
    try:
        if n_clicks > 0 and user_input:
            # Parse existing chat history into messages
            messages = [{"role": "system", "content": (
                "You are a career assistant integrated within a One-stop Career Exploration Dashboard, "
                "designed to help Australian job seekers and students find suitable career paths, employers, "
                "and relevant academic programs."
            )}]
            if chat_history:
                for line in chat_history.strip().split('\n'):
                    if line.startswith('User:'):
                        messages.append({"role": "user", "content": line[6:]})
                    elif line.startswith('ChatGPT:'):
                        messages.append({"role": "assistant", "content": line[8:]})

            # Add the user's new message
            messages.append({"role": "user", "content": user_input})

            # Call OpenAI API to generate a response
            if client is None:
                chat_history += f'User: {user_input}\n'
                chat_history += 'ChatGPT: (Chat feature is disabled — no OpenAI API key configured.)\n'
                return chat_history
    
            response = client.chat.completions.create(model='gpt-4', messages=messages)
            assistant_reply = response.choices[0].message.content

            # Update the chat history
            chat_history += f'User: {user_input}\n'
            chat_history += f'ChatGPT: {assistant_reply}\n'

            return chat_history
        else:
            return chat_history
    except Exception as e:
        print(f'Error in callback: {e}')
        return chat_history






import os

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=False)
