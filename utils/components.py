import dash_bootstrap_components as dbc


def create_navbar():
    return dbc.NavbarSimple(
        brand="Swing Vision",
        brand_href="#",
        color="#2E8B57",
        dark=True,
        fluid=True,
        className='ps-4'
    )