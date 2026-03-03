from flask import Flask, jsonify
from config import Config
import os
from extensions import db, jwt,mail
from flask_cors import CORS
from sqlalchemy import text
from routes.auth_routes import auth_bp
from routes.tower_routes import tower_bp
from routes.unit_routes import unit_bp
from routes.booking_routes import booking_bp
from routes.lease_routes import lease_bp
from models.lease import Lease
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    jwt.init_app(app)
    # CORS configured after blueprints (see below)
    mail.init_app(app)
    # with app.app_context():
    #     Lease.__table__.create(bind=db.engine)
    #registrations of blue_print
    app.register_blueprint(auth_bp,url_prefix='/auth')
    app.register_blueprint(tower_bp,url_prefix='/towers')
    app.register_blueprint(unit_bp,url_prefix='/units')
    app.register_blueprint(booking_bp,url_prefix='/bookings')
    app.register_blueprint(lease_bp,url_prefix='/leases')

    # Explicit CORS — must be after all blueprints are registered
    CORS(app,
         origins=["http://localhost:4200", "http://127.0.0.1:4200"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
         allow_headers=["Content-Type", "Authorization"],
         supports_credentials=True)
    from models.tower import Tower
    from models.unit import Unit

    @app.route("/public/stats")
    def public_stats():
        try:
            tower_count = Tower.query.count()
            unit_count  = Unit.query.count()
            return jsonify({
                "towers": tower_count,
                "units":  unit_count
            })
        except Exception as e:
            return jsonify({"towers": 0, "units": 0}), 200

    @app.route("/")
    def test_db():
        try:
            db.session.execute(text("SELECT 1"))
            print("DB Connected success")
            return jsonify({"message": "Database connected successfully!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return app


app = create_app()

# if __name__ == "__main__":
#     app.run(debug=True)
#     app.run(host='0.0.0.0', port=5000)
