from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__, static_url_path="", static_folder="static")
CORS(app)

@app.route("/")
def default():
	return app.send_static_file("html/index.html")

@app.route("/hello")
def hello():
	return jsonify({
		"message": "Hello, World!"
	})

@app.route("/hello-list")
def hello_list():
	return jsonify([
		{ "message": "こんにちは" },
		{ "message": "hello" },
		{ "message": "guten tag" }
	])

if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=8000)