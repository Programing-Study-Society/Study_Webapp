from sqlalchemy import create_engine, Column, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#接続先のDB
DATABASE = 'sqlite:///todo.sqlite3'

#Engineの作成
Engine = create_engine(
    DATABASE,
    echo=False,
    connect_args={"check_same_thread": False}
)

d_base = declarative_base()

class Todo(d_base):
    __tablename__ = 'todo'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255))
    description = Column(Text)

    def to_dict(self):
        todo = {
            "id": self.id,
            "title": self.title,
            "description": self.description
        }
        
        return todo
    

def create_database():
    d_base.metadata.create_all(bind=Engine)
    
def create_session():
    return sessionmaker(bind=Engine)()

if __name__ == "__main__":
    create_database()
        