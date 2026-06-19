import os.path
from datetime import datetime, timedelta
import os
from flask import Flask, render_template, request, jsonify, session, redirect,g,send_from_directory
from flask_mail import Message
import config
from exts import db, migrate, mail
from models import User,VegetableCategory,Vegetable,EmailCode
import random
import string
import commands
from decorators import login_required
import uuid
from dlmodel import  predict

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
migrate.init_app(app, db)
mail.init_app(app)
app.cli.command("init-category")(commands.init_vegetable_category)

# 获取当前文件所在目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 配置 media_dir
app.config['media_dir'] = os.path.join(BASE_DIR, 'media')

# 创建 media 文件夹（如果不存在）
if not os.path.exists(app.config['media_dir']):
    os.makedirs(app.config['media_dir'])

# ========== 路由 ==========
@app.before_request
def before_request():
    user_id = session.get('user_id')
    if user_id:
        user=db.session.get(User,user_id)
        g.user=user
    else:
        g.user=None

@app.context_processor
def context_processor():
    categories = db.session.execute(db.select(VegetableCategory)).scalars().all()
    return {
         "user":g.user,
        "categories":categories
    }

@app.route('/')
def index():
    category_id=request.args.get('category')
    categories = db.session.scalars(db.select(VegetableCategory)).all()
    if category_id:
        stmt=db.select(Vegetable).where(Vegetable.category_id==category_id)
    else:
        stmt=db.select(Vegetable)

    vegetables = db.session.scalars(stmt.order_by(Vegetable.pub_date.desc())).all()
    return render_template('index.html',
                           vegetables=vegetables,
                           category_id=category_id,
                           categories=categories)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        user=db.session.scalar(db.select(User).where(User.email == email))
        if user and user.check_password(password):
            session['user_id'] = user.id
            if remember :
                session.permanent = True
            return redirect("/")
        else:
            print("邮箱或密码错误，请重新登录")
            return redirect("/login")


@app.post('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        code = request.form.get('code')
        code_model=db.session.scalar(db.select(EmailCode).where(EmailCode.email==email,EmailCode.code==code))
        if not code_model or (datetime.now()-code_model.creat_time)>timedelta(minutes=10):
            return jsonify({"result":False,"message":"请输入正确的验证码"})
        user=User(email=email,username=username,password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"result":True,"message":None})

@app.route('/pub',methods=['GET','POST'])
@login_required
def pub():
    if request.method == 'GET':
         categories =db.session.scalars(db.select(VegetableCategory)).all()
         return render_template('pub.html',categories=categories)
    else:
        picture = request.form.get('picture')
        category_id = request.form.get('category')
        name=request.form.get('name')
        content=request.form.get('content')
        price=request.form.get('price')
        place=request.form.get('place')
        provider=request.form.get('provider')
        mobile=request.form.get('mobile')

        vegetable=Vegetable(
            picture=picture,
            category_id=category_id,
            name=name,
            content=content,
            price=float(price) if price else 0.0,
            place=place,
            provider=provider,
            mobile=mobile,
            publisher=g.user
        )
        db.session.add(vegetable)
        db.session.commit()
        return redirect("/")






@app.post('/upload/picture')
def upload_picture():
    picture = request.files.get('picture')
    #图片重新命名
    new_name=picture.filename.split('.')[-1]
    filename=f"{uuid.uuid4()}.{new_name}"
    picture_path=os.path.join(app.config['media_dir'], filename)
    picture.save(picture_path)
    #预测蔬菜分类
    category_name=predict(picture_path)
    category=db.session.scalar(db.select(VegetableCategory).where(VegetableCategory.name==category_name))

    return jsonify({
        "result":True,
        "filename":filename,
        "category":{"id":category.id,"name":category.name},
    })




@app.get('/email/code')
def getEmail():
    email = request.args.get('email')
    if not email:
        return jsonify({"result": False, "message": "请传入邮箱!"})
    source = string.digits * 4
    ans = "".join(random.sample(source, 4))
    message = Message(
        subject="知了蔬菜供应商-验证码",
        recipients=[email],
        body=f"你的验证码是{ans}"
    )
    try:
        mail.send(message)
    except Exception as e:
        return jsonify({"result": False, "message": str(e)})
    code_email=EmailCode(code=ans,email=email)
    db.session.add(code_email)
    db.session.commit()
    return jsonify({"result": True, "message": None})

@app.route('/detail/<int:vegetable_id>')
def detail(vegetable_id):
    vegetable=db.session.get(Vegetable,vegetable_id)
    return render_template('detail.html',vegetable=vegetable)

@app.route('/media/<filename>')
def media(filename):
    return send_from_directory(app.config['media_dir'], filename)




if __name__ == '__main__':
    app.run()