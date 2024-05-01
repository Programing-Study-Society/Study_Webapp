from flask import Blueprint, jsonify, request
import sys
sys.path.append("../")
from database import create_session, Todo

router = Blueprint("API", __name__, url_prefix="/api")

class TodoPostValueError(Exception):
    pass

class TodoNotFoundError(Exception):
    pass

@router.route("/post", methods=["POST"])
def post():
    try: 
        print(request.json)
        title = request.json["title"]
        description = request.json["description"]
        
        if (title is None) or (description is None) or (title == "") or (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        if len(title) > 255:
            raise TodoPostValueError("タイトルの文字数は255文字以内にしてください。")
        
        
        session = create_session()
        todo = Todo(
            title = title,
            description = description
        )
        session.add(todo)
        session.commit()
        
        
        return jsonify({
            "result": True
        })
    except TodoPostValueError as e:
        print(e)
        return jsonify({
            "result": False,
            "message": e.args[0],
        }), 400
    except Exception as e:
        print(e)
        return jsonify({
            "result": False,
            "message": "Internal Server Error"
        }), 500

@router.route("/todos")
def get_todos():
    try:
        session = create_session()
        todos = session.query(Todo).all()
        for todo in todos:
            print(todo)
        return jsonify([todo.to_dict() for todo in todos])
    except:
        return jsonify([]), 500

@router.route("/todo/<int:_id>")
def get_todo(_id):
    try:
        session = create_session()
        todo =  session.query(Todo).filter(Todo.id == _id).first()
        if todo is None:
            raise TodoNotFoundError("Todoがありません")
        
        
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
        
@router.route("/update", methods=["POST"])
def update():
    try:
        title = request.json["title"]
        description = request.json["description"]
        _id = request.json["id"]
        
        if _id is None:
            raise TodoPostValueError("idを入力してください。")
        
        if (title is None) and (description is None) or (title == "") and (description == ""):
            raise TodoPostValueError("タイトルと詳細を入力してください。")
        
        if title:
            if len(title) > 255:
                raise TodoPostValueError("タイトルの文字数は255文字以下にしてください。")
            
        
        session = create_session()
        todo = session.query(Todo).filter(Todo.id == _id).first()
        if todo is None:
            raise TodoNotFoundError("Todoがありません")
        
        if title:
            todo.title = title
            
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
        