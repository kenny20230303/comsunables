from sqlalchemy import create_engine, Column, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# 连接到数据库
db_name = "local_sqlite.db"
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, db_name)

engine = create_engine(f'sqlite:///{db_path}', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# 添加warehouse_type列到Material表
try:
    # 使用text()函数将SQL语句明确声明为文本
    sql = text('ALTER TABLE Material ADD COLUMN warehouse_type VARCHAR(200) DEFAULT "事务所仓库"')
    session.execute(sql)
    session.commit()
    print("成功添加warehouse_type列到Material表")
except Exception as e:
    session.rollback()
    print(f"添加列时出错: {e}")
finally:
    session.close()