from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from rich.console import Console
from rich.table import Table

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

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