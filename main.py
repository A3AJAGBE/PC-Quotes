# Imports
from flask import Flask

# Create an instance of flask
app = Flask(__name__)

# TODO: Remove debug in production
if __name__ == '__main__':
    app.run(debug=True)
