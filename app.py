from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
import config
from exts import db,migrate
import models
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate.init_app(app,db)

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
