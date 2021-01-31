# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dbinfo
from flask_marshmallow import Marshmallow

# Create an instance of flask
app = Flask(__name__)

# Database setup
dblink = 'mysql+pymysql://{0}:{1}@{2}/{3}'.format(
    dbinfo.user, dbinfo.password, dbinfo.host, dbinfo.database)

app.config['SQLALCHEMY_DATABASE_URI'] = dblink
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Instantiate marshmallow
"""This is used to parse post objects into a JSON response."""
ma = Marshmallow(app)


# Database model - Creating a Quotes table
class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"Quote: {self.quote}"


# Marshmallow schema based on model
class QuotesSchema(ma.Schema):
    class Meta:
        # Field to expose
        fields = ["quote"]
        model = Quotes


quotes_schema = QuotesSchema()

# TODO: Remove debug in production
if __name__ == '__main__':
    app.run(debug=True)
