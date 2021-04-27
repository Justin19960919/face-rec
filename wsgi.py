from app import app
from flask_sqlalchemy import SQLAlchemy


if __name__ == "__main__":
    db = SQLAlchemy(app)
    db.create_all()
    app.run()
