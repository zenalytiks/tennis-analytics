from config import app
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import callbacks
from utils.components import create_navbar



app.layout = html.Div(
    [
        create_navbar(),
        dbc.Container(
            [
                dash.page_container,
            ],fluid=True,className='main-content'
        )
    ]
)

if __name__ == '__main__':
    app.run(debug=False,port=8080)