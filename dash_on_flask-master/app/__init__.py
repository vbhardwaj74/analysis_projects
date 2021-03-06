import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from flask import Flask
from flask.helpers import get_root_path
from flask_login import login_required
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
import dash_bootstrap_components as dbc
from config import BaseConfig

def create_app():
    server = Flask(__name__)
    server.config.from_object(BaseConfig)

    register_dashapps(server)
    register_extensions(server)
    register_blueprints(server)

    return server


def register_dashapps(app):
    #import app.dashapp1.single_page_app
    from app.dashapp1.layout import layout
    from app.dashapp1.callbacks import register_callbacks

    # Meta tags for viewport responsiveness
    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp1 = dash.Dash(__name__,
                         external_stylesheets=['https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/solar/bootstrap.min.css'],
                         server=app,
                         url_base_pathname='/dash/',
                         assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                         meta_tags=[meta_viewport])
    Bootstrap(app)

    with app.app_context():
        dashapp1.title = 'Dashapp'
        dashapp1.layout = layout
        register_callbacks(dashapp1)

    _protect_dashviews(dashapp1)


def _protect_dashviews(dashapp):
    for view_func in dashapp.server.view_functions:
        if view_func.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_func] = login_required(dashapp.server.view_functions[view_func])


def register_extensions(server):
    from app.extensions import db
    from app.extensions import login
    from app.extensions import migrate

    db.init_app(server)
    login.init_app(server)
    login.login_view = 'main.login'
    migrate.init_app(server, db)


def register_blueprints(server):
    from app.webapp import server_bp

    server.register_blueprint(server_bp)
