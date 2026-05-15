from flask import Flask
from .extensions import db, login_manager
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY']                     = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI']        = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import models
        from app.models import Trabajador

        @login_manager.user_loader
        def load_user(user_id):
            return Trabajador.query.get(int(user_id))

        from app.auth import auth_bp
        from app.main import main_bp
        from app.productos import productos_bp
        from app.proveedores import proveedores_bp
        from app.inventario import inventario_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(main_bp)
        app.register_blueprint(productos_bp)
        app.register_blueprint(proveedores_bp)
        app.register_blueprint(inventario_bp)

    return app