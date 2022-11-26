from flask import Flask
from waitress import serve
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_httpauth import HTTPBasicAuth

load_dotenv()
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234567890@localhost/lab_schema'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()

# import src.model.user
# import src.model.playlist
# import src.route.users
# import src.route.playlists


@app.before_request
def create_tables():
    db.create_all()


if __name__ == "__app__":
    app.run()
