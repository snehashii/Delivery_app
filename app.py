from flask import Flask
from config import Config
from extensions import db
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app) 

    db.init_app(app)

    # 🔹 Register Blueprints
    from routes.roles import roles_bp
    from routes.users import users_bp
    from routes.permissions import permissions_bp
    from routes.role_permission import role_permissions_bp
    from routes.user_hierarchy import user_hierarchy_bp
    from routes.riders import riders_bp
    from routes.deliveries import deliveries_bp
    from routes.third_party_service import third_party_bp
    from routes.tracking import tracking_bp
    from routes.inventory import inventory_bp

    app.register_blueprint(roles_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(permissions_bp)
    app.register_blueprint(role_permissions_bp)
    app.register_blueprint(user_hierarchy_bp)
    app.register_blueprint(riders_bp)
    app.register_blueprint(deliveries_bp)
    app.register_blueprint(third_party_bp)
    app.register_blueprint(tracking_bp)
    app.register_blueprint(inventory_bp)

    @app.route('/')
    def home():
        return "✅ Delivery App Backend is Running"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
