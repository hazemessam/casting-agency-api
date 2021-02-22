# Third party imports
from flask import Flask
from flask_cors import CORS

# Application imports
from models import setup_db


# Setup the application
app = Flask(__name__)
setup_db(app)
CORS(app)

from views import *

if __name__ == '__main__':
    app.run(port=8080, debug=True)
