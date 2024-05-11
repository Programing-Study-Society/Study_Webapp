from flask import Blueprint, jsonify, request
import sys
# 別のディレクトリにあるモジュールをインポートするためのパスを追加
sys.path.append("../")
from database import Todo, get_all_todos, get_filtering_todo, update_todo, add_todo, delete_todo, exist_todo

# ファイルを分割する機能
# /apiに色々なパスを追加する機能
router = Blueprint("API", __name__, url_prefix="/api")

### エラーの定義
# 値が不適切な場合のエラー
class TodoPostValueError(Exception):
    pass

# Todoが見つからないときのエラー
class TodoNotFoundError(Exception):
    pass


### /api/todosの定義
# 全てのtodoを返す
@router.route("/todos")
def get_todos():
    try:
        # データベースのTodoから全データを取得
        todos = get_all_todos()
        
        # 全てのtodoを返す
        return jsonify({
            "result": True,
            # todosからtodoを一つずつ取り出し辞書型にする
            "todos": [todo.to_dict() for todo in todos]
        })
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500


### /api/postの定義
# todoを作成する
# route("パスの指定", methods=["HTTPメソッドの指定"])
@router.route("/post", methods=["POST"])
def post():
    try: 
        # jsonデータの取得
        title = request.json["title"]
        description = request.json["description"]
        
        # 入力データがない場合
        if (title is None) or (description is None) or (title == "") or (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        # データの文字数がオーバーした場合
        if len(title) > 255:
            raise TodoPostValueError("タイトルの文字数は255文字以内にしてください。")
        
        # データベースにTodoを追加する
        add_todo(title, description)
        
        # todoの作成が成功したことを伝える
        return jsonify({
            "result": True
        })
        
    # 不適切なデータである場合のエラー
    except TodoPostValueError as e:
        print(e)
        # jsonデータとステータスコード
        return jsonify({
            "result": False,
            "message": e.args[0],
        }), 400
    # 予期しないエラー
    except Exception as e:
        print(e)
        # jsonデータとステータスコード
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500


### /api/todo/<int:_id>の定義
# idで指定されたtodoを返す
# /todo/<int:_id>とすることでパスで指定したidをプログラム内で扱える
# 例 : /todo/1 → idが1のtodoを取得
@router.route("/todo/<int:_id>")
def get_todo(_id):
    try:
        # 指定したtodoがない場合
        if not exist_todo(_id):
            raise TodoNotFoundError("Todoがありません")
        
        # idが一致するTodoを取得
        todo = get_filtering_todo(Todo.id == _id)
        
        # 見つかったtodoを返す
        return jsonify({
            "result": True,
            "todo": todo.to_dict()
        })
    # todoがない場合のエラー
    except TodoNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "todoがありません"
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500


### /api/updateの定義
# idで指定されたtodoの内容を変更する
@router.route("/update", methods=["POST"])
def update():
    try:
        # jsonデータの取得
        title = request.json["title"]
        description = request.json["description"]
        _id = request.json["id"]
        
        # _idがない場合
        if _id is None:
            raise TodoPostValueError("idを入力してください。")
        
        # 入力したデータがない場合
        if (title is None) and (description is None) or (title == "") and (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        # titleの文字数がオーバーしていた場合
        if len(title) > 255:
            raise TodoPostValueError("タイトルの文字数は255文字以下にしてください。")
        
        # todoがない場合
        if not exist_todo(_id):
            raise TodoNotFoundError("Todoがありません")
        
        update_todo(_id, title, description)
        
        # 変更できたことを伝える
        return jsonify({
            "result": True
        })
    except TodoPostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 400
    except TodoNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500


### /api/deleteの定義
# idで指定されたtodoの削除
@router.route("/delete", methods=["DELETE"])
def delete():
    try:
        _id = request.json["id"]
        
        if _id is None:
            raise TodoPostValueError("idを入力してください")
        
        if not exist_todo(_id):
            raise TodoNotFoundError("Todoがありません")
        
        # todoの削除
        delete_todo(_id)
        
        return jsonify({
            "result": True
        })
    
    except TodoPostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 400
    except TodoNotFoundError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0]
        }), 404
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500
