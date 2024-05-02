from flask import Blueprint, jsonify, request
import sys
# 別のディレクトリにあるモジュールをインポートするためのパスを追加
sys.path.append("../")
from database import create_session, Todo

# ファイルを分割する機能
# /apiに色々なパスを追加する機能
router = Blueprint("API", __name__, url_prefix="/api")

#エラーの定義
class TodoPostValueError(Exception):
    pass

class TodoNotFoundError(Exception):
    pass

# /api/post, methodの定義
@router.route("/post", methods=["POST"])
def post():
    try: 
        print(request.json)
        
        # jsonデータの取得
        title = request.json["title"]
        description = request.json["description"]
        
        # 入力したデータがない場合のエラーを出力
        if (title is None) or (description is None) or (title == "") or (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        # データの文字数がオーバー場合のエラーを出力
        if len(title) > 255:
            raise TodoPostValueError("タイトルの文字数は255文字以内にしてください。")
        
        
        # セッションを作成してデータベースと接続できるようにする
        # 以後データベースはDBとする
        session = create_session()
        
        # todoを作成する
        todo = Todo(
            title = title,
            description = description
        )
        
        # データベースにtodoを追加
        session.add(todo)
        session.commit()
        
        # todoの作成が成功した場合に返すjsonデータ
        return jsonify({
            "result": True
        })
        
    # データがない場合のエラーが発生したとき
    except TodoPostValueError as e:
        print(e)
        # jsonデータとステータスコード
        return jsonify({
            "result": False,
            "message": e.args[0],
        }), 400
    # 予期しないエラーが発生したとき
    except Exception as e:
        print(e)
        # jsonデータとステータスコード
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

# /api/todosの定義
@router.route("/todos")
def get_todos():
    try:
        session = create_session()
        # データベースのTodoから全データを取得
        todos = session.query(Todo).all()
        
        # todosからtodoを一つずつ取り出し辞書型にして返す
        return jsonify([todo.to_dict() for todo in todos])
    except:
        # todoがない場合に返すjsonデータとステータスコード
        return jsonify([]), 500

# /api/todo<int:_id>の定義
@router.route("/todo/<int:_id>")
def get_todo(_id):
    try:
        session = create_session()
        
        # DBのidと/api/todo/_idと一致したtodoを昇順で取り出す
        todo =  session.query(Todo).filter(Todo.id == _id).first()
        
        # todoがない場合のエラー
        if todo is None:
            raise TodoNotFoundError("Todoがありません")
        
        # todoが見つかった場合に返すjsonデータ
        return jsonify({
            "result": True,
            "todo": todo.to_dict()
        })
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

# /api/update、methodの定義
@router.route("/update", methods=["POST"])
def update():
    try:
        
        # jsonデータの取得
        title = request.json["title"]
        description = request.json["description"]
        _id = request.json["id"]
        
        # _idがない時のエラー
        if _id is None:
            raise TodoPostValueError("idを入力してください。")
        
        # 入力したデータがない場合のエラー
        if (title is None) and (description is None) or (title == "") and (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        # titleがある場合、titleの文字数がオーバーしていた場合エラーを返す
        if title:
            if len(title) > 255:
                raise TodoPostValueError("タイトルの文字数は255文字以下にしてください。")
            
        
        session = create_session()
        
        # Todoのidと取得としたidが一致todoを昇順で取り出す
        todo = session.query(Todo).filter(Todo.id == _id).first()
        
        # todoがない場合のエラー
        if todo is None:
            raise TodoNotFoundError("Todoがありません")
        
        # todoのtitleがある場合、titleを入れる
        if title:
            todo.title = title
        
        # todoの詳細がある場合、詳細を入れる
        if description:
            todo.description = description
            
        session.commit()
        
        
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

# /api/delete,methodの定義
@router.route("/delete", methods=["DELETE"])
def delete():
    try:
        _id = request.json["id"]
        
        if _id is None:
            raise TodoPostValueError("idを入力してください")
        
        session = create_session()
        todo = session.query(Todo).filter(Todo.id == _id).first()
        if todo is None:
            raise TodoNotFoundError("Todoがありません")
        
        session.delete(todo)
        session.commit()
        
        
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
        