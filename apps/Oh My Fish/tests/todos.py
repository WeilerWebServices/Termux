import os

from flask import Flask

def create_app(test_config=None):
    """Factory to configure and return a Flask application.
    Keyword arguments:
    test_config -- dictionary to configure the app for tests (default None)
    """

    # Create the Flask application object using this module's name
    app = Flask(__name__)

    # Configure App
    # -------------
    # Default configuration, can be overwritten by specific environment
    app.config.from_mapping(
        SECRET_KEY="dev",
        DB_URL="postgresql://flasktodo_user@localhost/flasktodo",
        DB_SSLMODE="allow",
    )

    if test_config is None:
        # App configuration for dev or prod if `config.py` exists
        app.config.from_pyfile("config.py", silent=True)

        # Check for environment variables on Heroku
        prod_db_url = os.environ.get("DATABASE_URL", None)
        if prod_db_url is not None:
            app.config.from_mapping(
                DB_URL=prod_db_url,
                DB_SSLMODE="require"
            )
    else:
        # App configuration specifically for tests
        app.config.from_mapping(test_config)

    # Setup Database
    # --------------
    from . import db
    db.init_app(app)

    # Register Routes
    # ---------------
    from . import todos
    app.register_blueprint(todos.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    # Return application object to be used by a WSGI server, like gunicorn
    return app
