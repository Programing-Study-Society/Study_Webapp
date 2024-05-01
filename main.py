from flask import Flask, redirect
from flask_cors import CORS

from database import create_database
from routes.API import router as API_route


create_database()
app = Flask(__name__, static_url_path="", static_folder="static")
app.register_blueprint(API_route)
CORS(app)


@app.route("/")
def index():
    return redirect("/html/index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)