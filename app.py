"""
Life Tracker Flask application factory.

Keeps instantiation (Flask wiring) separate from routing, services, and templates.
"""

from __future__ import annotations

import os

from flask import Flask


def create_application() -> Flask:
    package_dir = os.path.abspath(os.path.dirname(__file__))

    flask_app = Flask(
        __name__,
        template_folder=os.path.join(package_dir, "templates"),
        static_folder=os.path.join(package_dir, "static"),
    )

    from routes.analysis_routes import analysis_bp
    from routes.api_routes import api_bp
    from routes.home_routes import home_bp

    flask_app.register_blueprint(home_bp)
    flask_app.register_blueprint(analysis_bp)
    flask_app.register_blueprint(api_bp)

    flask_app.config.setdefault("JSON_SORT_KEYS", False)
    flask_app.config.setdefault(
        "SEND_FILE_MAX_AGE_DEFAULT",
        int(os.getenv("SEND_FILE_MAX_AGE_DEFAULT", "31536000")),
    )

    return flask_app


app = create_application()


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5001"))
    debug = os.getenv("FLASK_DEBUG", "true").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }
    app.run(host="127.0.0.1", port=port, debug=debug)
