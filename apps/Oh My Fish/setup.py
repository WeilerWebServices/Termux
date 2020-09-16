web: flask init-db; gunicorn "flasktodo:create_app()"
