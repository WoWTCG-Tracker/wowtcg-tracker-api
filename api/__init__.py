import flask
import os
from dotenv import load_dotenv

load_dotenv()
app = flask.Flask(__name__)
if os.getenv('FLASK_ENV') == 'development':
    app.config['DEBUG'] = True

@app.route("/", methods=["GET"])
def api_root():
    return "Hello world!"

if __name__ == "__main__":
    app.run()
