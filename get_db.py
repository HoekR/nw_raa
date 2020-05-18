from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from .config import get_config

#app = Flask(__name__)
app = Flask(__name__, static_url_path='', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = get_config(host="local")
db = SQLAlchemy(app)
Base = automap_base()
Base.prepare(db.engine, reflect=True)

