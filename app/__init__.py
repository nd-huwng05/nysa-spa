from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from rich.console import Console
from rich.table import Table
from flask_migrate import Migrate
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
jwt = JWTManager(app)
oauth = OAuth(app)

oauth.register(
name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile'}
)

from app.user.models import *
from app.home.models import *
from app.customer.models import *
from app.voucher.models import *
from app.staff.models import *
from app.invoice.models import *
from app.service.models import *
from app.booking.models import *
migrate = Migrate(app, db)

from app.home.routes import register_routes
register_routes()

from app.user.routes import register_routes
register_routes()

from app.booking.routes import register_routes
register_routes()

from app.service.routes import register_routes
register_routes()

from app.voucher.routes import register_routes
register_routes()

from app.invoice.routes import register_routes
register_routes()

from app.customer.routes import register_routes
register_routes()

from app.staff.routes import register_routes
register_routes()


def print_all_routes():
    console = Console()
    table = Table(title="SPA BEAUTIFULLY ROUTES")

    table.add_column("Methods", style="cyan", no_wrap=True)
    table.add_column("Path", style="green")
    table.add_column("Endpoint", style="magenta")

    for rule in app.url_map.iter_rules():
        methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
        table.add_row(methods, rule.rule, rule.endpoint)

    console.print(table)

print_all_routes()