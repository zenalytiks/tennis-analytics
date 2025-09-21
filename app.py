from config import app
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import callbacks
from utils.components import create_navbar

server = app.server

app.layout = html.Div(
    [
        create_navbar(),
        dbc.Container(
            [
                dash.page_container,
            ],fluid=True,className='main-content',style={'background-color':'#F8F9FA'}
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=True,port=8080)