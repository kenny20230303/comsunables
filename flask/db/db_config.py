from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from datetime import datetime

db_name = "local_sqlite.db"
current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(current_dir, db_name)

engine = create_engine(f'sqlite:///{db_path}', echo=False, future=True)
session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# todo 用户 部门
class UserDepartment(BaseModel):
    __tablename__ = 'UserDepartment'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)


# todo 供应商 管理
class Supplier(BaseModel):
    __tablename__ = 'Supplier'
    id = Column(Integer, primary_key=True)
    number = Column(String(200), nullable=True)  # 编号
    name = Column(String(200), nullable=True)  # 联系人
    phone = Column(String(200), nullable=True)  # 电话号码
    address = Column(String(200), nullable=True)  # 地址


# todo 材料信息 管理
class Material(BaseModel):
    __tablename__ = 'Material'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)  # 名称
    specifications = Column(String(200), nullable=True)  # 规格
    unit = Column(String(200), nullable=True)  # 单位
    price = Column(String(200), nullable=True)  # 单价
    Supplier_id = Column(String(200), nullable=True)  # 供应商
    secure_days = Column(String(200), nullable=True)  # 安全在库
    secure_number = Column(String(200), nullable=True)  # 安全在库
    number = Column(String(200), default='0')
    warehouse_type = Column(String(200), default='事务所仓库')  # 仓库类型：事务所仓库/工厂消耗品仓库


class MaterialHistory(BaseModel):
    __tablename__ = 'MaterialHistory'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)  # 名称
    specifications = Column(String(200), nullable=True)  # 规格
    unit = Column(String(200), nullable=True)  # 单位
    price = Column(String(200), nullable=True)  # 单价
    Supplier_id = Column(String(200), nullable=True)  # 供应商
    number = Column(String(200), default='0')
    type = Column(String(200), default='入库')
    current_time = Column(String(200), default=datetime.now().strftime('%Y-%m-%d %H:%M'))


# todo 月计划申请 管理
class MonthlyPlan(BaseModel):
    __tablename__ = 'MonthlyPlan'
    id = Column(Integer, primary_key=True)
    MonthlyPlan_type = Column(String(200), default='计划内')  # (计划内，计划外)
    user_id = Column(String(200), nullable=True)  # 用户信息 id
    Material_id = Column(String(200), nullable=True)  # 材料信息 id
    Material_number = Column(String(200), nullable=True)  # 材料数量

    auditor = Column(String(200), default='False')  # 审核员审核
    finance = Column(String(200), default='False')  # 财务审核

    naqi = Column(String(200), default='')
    beizhu = Column(String(200), default='')

    number_change = Column(String(200), default='False')

    current_time = Column(String(200), default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    belong_month = Column(String(200), default=datetime.now().strftime('%Y-%m-%d'))


# todo 每日消耗计划申请 管理
class DailyApplication(BaseModel):
    __tablename__ = 'DailyApplication'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(200), nullable=True)  # 用户信息 id
    Material_id = Column(String(200), nullable=True)  # 材料信息 id
    Material_number = Column(String(200), nullable=True)  # 材料数量

    auditor = Column(String(200), default='False')  # 审核员审核
    finance = Column(String(200), default='False')  # 财务审核

    number_change = Column(String(200), default='False')

    current_time = Column(String(200), default=datetime.now().strftime('%Y-%m-%d %H:%M'))
    belong_month = Column(String(200), default=datetime.now().strftime('%Y-%m-%d'))


class User(BaseModel):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(200), nullable=True)
    password = Column(String(200), nullable=True)
    name = Column(String(200), nullable=True)
    phone = Column(String(200), nullable=True)
    user_type = Column(String(200), default='user')  # (user,auditor,finance,admin)
    UserDepartment_name = Column(String(200), default='无')  # 用户部门


if __name__ == '__main__':
    # # 创建数据库
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with db_session() as session:
        to_user = User(username='admin', password='admin', user_type='admin')
        db_session.add(to_user)
        db_session.commit()
