import os
from backend.app import create_app
from backend.app.extensions import db

app = create_app()

with app.app_context():
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    using_neon = uri.startswith("postgresql+psycopg://")
    print("database=neon-postgres" if using_neon else "database=local-sqlite")
    if not os.getenv("DATABASE_URL"):
        print("DATABASE_URL is not set; local SQLite fallback is active.")
    with db.engine.connect() as con:
        result = con.exec_driver_sql("select 1").scalar()
        print(f"connection_ok={result == 1}")
