from config import app
import dash
import dash_bootstrap_components as dbc
from dash import html
import callbacks
from utils.components import create_navbar

server = app.server

app.layout = html.Div(
    [
        create_navbar(),
        dbc.Container(
            [
                dash.page_container,
            ],fluid=True,style={'background-color':'#F8F9FA'}
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=False,port=8080)