from flask import Flask, redirect
from flask_cors import CORS
from database import create_database
# routesフォルダのAPI.py内からrouterをimportしてAPI_routeに名前を変更
from routes.API import router as API_route


# database.pyから持ってきたcreate_databaseを実行
create_database()
# appにFlaskのアプリ名、
# staticフォルダのパス(今回はmain.pyと同じ階層なので、"")
# static_folderの名前を入れている
app = Flask(__name__, static_url_path="", static_folder="static")
# appにBlueprintを登録
# API_route(今回では、"/api/～"を渡している)
app.register_blueprint(API_route)
# appにCORSを適用
CORS(app)

# 始めに表示されるページ
@app.route("/")
def index():
    return redirect("/html/index.html")


# アプリケーションを起動
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)