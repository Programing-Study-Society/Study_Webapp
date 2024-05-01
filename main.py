from flask import Flask
from database import create_database
from routes.API import router as API_route

create_database()
app = Flask(__name__, static_url_path="", static_folder="static")
app.register_blueprint(API_route)

@app.route("/")
def index():
    return app.send_static_file("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)