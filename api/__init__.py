"""API server for WoWTCG Tracker"""
import os
import flask
from dotenv import load_dotenv

load_dotenv()
app = flask.Flask(__name__)
if os.getenv('FLASK_ENV') == 'development':
    app.config['DEBUG'] = True

@app.route("/", methods=["GET"])
def api_root():
    """API root"""
    return "Hello world!"

if __name__ == "__main__":
    app.run()
