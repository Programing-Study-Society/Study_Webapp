from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql._typing import _ColumnExpressionArgument

#接続先のDB
DB = 'sqlite:///todo.sqlite3'

#DBに接続するためのEngineの作成
Engine = create_engine(
    DB,
    #sql文のログの出力しないように設定している
    echo=False,
    # sqliteを使用する時に複数スレッドの接続を許可している
    connect_args={"check_same_thread": False}
)

# ここで定義した変数を継承することで簡単にテーブルが作れるようになる
d_base = declarative_base()

# todoテーブルの作成
class Todo(d_base):
    # テーブル名の設定
    __tablename__ = 'todo'
    
    # カラムの作成
    # (カラムの型(最大値)、主キー、キーを1ずつ増やす)
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(Text)

    # DBの各値を辞書型にしている
    def to_dict(self):
        todo = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        
        return todo
    
# 全てのテーブルを作成
def create_database():
    d_base.metadata.create_all(bind=Engine)

# 新しいセッションを作成する関数
def create_session():
    return sessionmaker(bind=Engine)()


def get_all_todos():
    session = create_session()
    return session.query(Todo).all()


def get_filtering_todo(filter: _ColumnExpressionArgument[bool] = True):
    session = create_session()
    return session.query(Todo).filter(filter).first()


def add_todo(title: str, description: str):
    session = create_session()
    # todoを作成する
    todo = Todo(
        title = title,
        description = description
    )
    # データベースにtodoを仮追加
    session.add(todo)
    # データベースに反映
    session.commit()


def exist_todo(id: int):
    session = create_session()
    # DBから指定されたIDと同一のTodoを検索
    todo = session.query(Todo).filter(Todo.id == id).first()
    if todo is None:
        return False
    else:
        return True


def update_todo(id: int, title: str, description: str):
    session = create_session()
    # DBのidと指定されたidが一致する一番はじめのtodoを取り出す
    todo = session.query(Todo).filter(Todo.id == id).first()
    # todoの内容を更新する
    todo.title = title
    todo.description = description
    session.commit()


def delete_todo(id: int):
    session = create_session()
    todo = session.query(Todo).filter(Todo.id == id).first()
    # todoの仮削除
    session.delete(todo)
    # データベースに反映させる
    session.commit()


# database.pyそのものが実行された時
if __name__ == "__main__":
    # データベースを作成
    create_database()
    session = create_session()
    todos = [
        Todo(title="test1", description="テストデータ1です"),
        Todo(title="test2", description="テストデータ2です"),
        Todo(title="test3", description="テストデータ3です")
    ]
    for todo in todos :
        session.add(todo)
        
    session.commit()
