from flask import Flask, jsonify, render_template
from rich.console import Console
from rich.table import Table
from app.core.environment import Environment
from app.core.logger import logger
from app.modules.home import HomeModule
from app.modules.service import ServiceModule
from app.modules.user import UserModule


class Server:
    def __init__(self):
        self.app = Flask(__name__, template_folder='templates')
        self.app.config.from_object('config')

        logger.setup(self.app)
        logger.info("Logger System Initiated")

        self.env = Environment()
        self.env.init_app(self.app)

        self.setup_health_check()
        self.setup_error_handler()

        self.init_modules()
        self.init_models()

    def setup_health_check(self):
        @self.app.route('/health')
        def health_check():
            from datetime import datetime
            return jsonify({
                'status': 'ok',
                'message': 'Server is up and running',
                'timestamp': datetime.utcnow().isoformat()
            })

    def setup_error_handler(self):
        @self.app.errorhandler(500)
        def internal_server_error(e):
            try:
                self.env.db.session.rollback()
            except:
                pass

            return render_template('errors/500.html'),500

        @self.app.errorhandler(404)
        def not_found(e):
            return render_template('errors/404.html'),404


    def print_routes(self):
        console = Console()
        table = Table(title="NYSA ROUTES", show_header=True, header_style="bold magenta")

        table.add_column("Methods", style="cyan", no_wrap=True)
        table.add_column("Path", style="green")
        table.add_column("Endpoint", style="white")

        for rule in self.app.url_map.iter_rules():
            methods = ",".join(sorted(rule.methods - {"HEAD", "OPTIONS"}))
            table.add_row(methods, rule.rule, rule.endpoint)

        console.print(table)

    def init_modules(self):
        UserModule(self.app, self.env).register()
        HomeModule(self.app, self.env).register()
        ServiceModule(self.app, self.env).register()


    def init_models(self):
        with self.app.app_context():
            import app.modules.user.repository.models
            import app.modules.home.repository.models
            import app.modules.service.repository.models
            import app.modules.staff.repository.models
            import app.modules.customer.repository.models

    def start(self):
        self.print_routes()
        self.app.run()

def new_server() -> Server:
    return Server()