from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool, QueuePool
from contextlib import contextmanager

Base = declarative_base()

# class User(Base):
#     __tablename__ = 'user'
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     username = Column(String(20), nullable=False)
#     password = Column(String(20), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    age = Column(Integer)


"""
代码说明：
基础配置：
Base 是 SQLAlchemy 的基类，用于所有 ORM 模型。
User 是一个示例模型，用于演示数据库操作。
Database 类：

__init__ 方法初始化数据库连接。
create_tables 方法创建数据库表。
drop_tables 方法删除数据库表。
session_scope 提供一个事务范围，以确保数据库操作的原子性和一致性。
add_sample_data 方法插入样例数据。
add_record 方法添加记录。
get_record 方法获取单条记录。
get_all_records 方法获取所有记录。
update_record 方法更新记录。
delete_record 方法删除记录。
clear_table 方法清空表。
switch_database 方法切换数据库。
使用方法：
实例化 Database 类并传入数据库 URL。
调用 create_tables 方法创建表。
使用其他方法进行增删改查操作。
使用 switch_database 方法切换到其他数据库。
"""


class Database:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = self._create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def _create_engine(self, db_url):
        if 'sqlite' in db_url:
            return create_engine(db_url, echo=True, poolclass=NullPool)
        else:
            return create_engine(db_url, echo=True, pool_size=20, max_overflow=0)

    def create_tables(self):
        """创建数据库表"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """删除数据库表"""
        Base.metadata.drop_all(self.engine)

    @contextmanager
    def session_scope(self):
        """提供一个事务范围"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            session.close()

    def add_sample_data(self):
        """插入样例数据"""
        with self.session_scope() as session:
            sample_user = User(name="Alice", age=25)
            session.add(sample_user)

    def add_record(self, record):
        """添加记录"""
        with self.session_scope() as session:
            session.add(record)

    def get_record(self, model, record_id):
        """获取记录"""
        with self.session_scope() as session:
            return session.query(model).filter_by(id=record_id).first()

    def get_all_records(self, model):
        """获取所有记录"""
        with self.session_scope() as session:
            return session.query(model).all()

    def update_record(self, model, record_id, **kwargs):
        """更新记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=record_id).first()
            for key, value in kwargs.items():
                setattr(record, key, value)
            session.add(record)

    def delete_record(self, model, record_id):
        """删除记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=record_id).first()
            session.delete(record)

    def clear_table(self, model):
        """清空表"""
        with self.session_scope() as session:
            session.query(model).delete()

    def switch_database(self, new_db_url):
        """切换数据库"""
        self.db_url = new_db_url
        self.engine = self._create_engine(new_db_url)
        self.Session = sessionmaker(bind=self.engine)


# 示例用法
if __name__ == "__main__":
    db = Database('sqlite:///database.db')  # 使用 SQLite 数据库
    db.create_tables()
    db.add_sample_data()

    with db.session_scope() as session:
        user = session.query(User).filter_by(id=1).first()
        print(f"Retrieved User: {user.name}, {user.age}")

    db.update_record(User, 1, name="Bob", age=30)

    with db.session_scope() as session:
        users = session.query(User).all()
        for user in users:
            print(f"User: {user.name}, {user.age}")

    # db.delete_record(User, 1)

    # db.clear_table(User)

    # db.drop_tables()
