from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

import config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData

app = Flask(__name__)
app.config.from_object(config)

# base类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention = {
    "ix": "%(table_name)s_%(column_0_label)s",  # 索引
    "uq": "%(table_name)s_%(column_0_name)s",   # 唯一约束
    "ck": "%(table_name)s_%(constraint_name)s", # 检查约束
    "fk": "%(table_name)s_%(column_0_name)s_%(referred_table_name)s",  # 外键约束
    "pk": "%(table_name)s"                       # 主键约束
})

db = SQLAlchemy(app,model_class=Base)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/pub')
def pub():
    return render_template('pub.html')

@app.route('/detail/<int:vegetable_id>')
def detail(vegetable_id):
    return render_template('detail.html')


if __name__ == '__main__':
    app.run()
