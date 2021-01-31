# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dbinfo

# Create an instance of flask
app = Flask(__name__)

# Database setup
dblink = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    dbinfo.user, dbinfo.password, dbinfo.host, dbinfo.database)

app.config['SQLALCHEMY_DATABASE_URI'] = dblink
db = SQLAlchemy(app)


# Database model - Creating a Quotes table
class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"Quote: {self.quote}"


# TODO: Remove debug in production
if __name__ == '__main__':
    app.run(debug=True)
