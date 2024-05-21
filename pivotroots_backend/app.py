import os

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = '5w3v5cu42gs6g7tf'

cors = CORS(app, resources={r"/*": {"origins": "*"}})

from autho_blueprint import autho
app.register_blueprint(autho, url_prefix="/")

from data_blueprint import data
app.register_blueprint(data, url_prefix="/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)