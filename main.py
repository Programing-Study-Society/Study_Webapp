from flask import Flask, redirect
from flask_cors import CORS
# routesフォルダのAPI.pyからrouterをimportしてAPI_routeに名前を変更
from routes.API import router as API_route


### Webアプリの作成
# Flaskのアプリ名を設定、
# staticファイル（HTML, CSSなど）にアクセスするパスを設定
# staticファイルのディレクトリ（場所）を設定
app = Flask(__name__, static_url_path="", static_folder="static")
# appにBlueprintを登録
# API_route(今回では、"/api/～"を渡している)
app.register_blueprint(API_route)
# appにCORS（違うドメインからAPIにアクセスするための機能）を適用
CORS(app)

### / を定義
# 始めに表示されるページ
@app.route("/")
def index():
    return redirect("/html/index.html")


# Webアプリを起動
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8000)