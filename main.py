# Imports
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import dbinfo
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
import random

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

# Instantiate flask_restful
api = Api(app)


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


quote_schema = QuotesSchema()
quotes_schema = QuotesSchema(many=True)


# Restful resource
class QuoteResource(Resource):
    def get(self):
        """This function returns all quotes in the database."""
        # quote = Quotes.query.get_or_404(id)
        # return quote_schema.dump(quote)
        quotes = Quotes.query.all()
        quote = random.choice(quotes_schema.dump(quotes))
        return quote

    def post(self):
        """This functions add a new quote to the database."""
        new_quote = Quotes(
            quote=request.json['quote']
        )
        db.session.add(new_quote)
        db.session.commit()
        return quote_schema.dump(new_quote)

    def delete(self, id):
        """This functions deletes a quote in the database."""
        quote = Quotes.query.get_or_404(id)
        db.session.delete(quote)
        db.session.commit()
        return '', 204


# Register resource and define endpoint
# api.add_resource(QuoteResource, '/quotes/<int:id>')
api.add_resource(QuoteResource, '/quotes/')

# TODO: Remove debug in production
if __name__ == '__main__':
    app.run(debug=True)
