from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from flask_migrate import Migrate

# base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention = {
    "ix": "%(table_name)s_%(column_0_label)s",  # 索引
    "uq": "%(table_name)s_%(column_0_name)s",   # 唯一约束
    "ck": "%(table_name)s_%(constraint_name)s", # 检查约束
    "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # 外键约束
    "pk": "%(table_name)s"                       # 主键约束
})

db = SQLAlchemy(model_class=Base)
migrate = Migrate()