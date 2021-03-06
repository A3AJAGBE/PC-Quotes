# Imports
from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from config import Config
from flask_migrate import Migrate
import random

# Create an instance of flask
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Instantiate marshmallow
"""This is used to parse post objects into a JSON response."""
ma = Marshmallow(app)

# Instantiate flask_restful
api = Api(app)


# Add an home page
@app.route('/')
def home():
    quotes_count = Quotes.query.count()
    quotes = Quotes.query.all()
    quote = random.choice(quotes)
    return render_template('index.html', title='Home', quotes=quotes_count, quote=quote)


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
        """This function returns a random quote in the database."""
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


# Register resource and define endpoint
api.add_resource(QuoteResource, '/quotes/v1.0/')

if __name__ == '__main__':
    app.run()
