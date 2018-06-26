# # -* encoding:utf-8 *-
from flask import Flask,render_template,g,request,redirect,url_for,session
import config
from sqlalchemy import or_#查找功能
from models import User,Question,Answer
from exts import db
from werkzeug.security import generate_password_hash
from functools import wraps #导入一个不改变装饰器名字
from flask_sqlalchemy import SQLAlchemy
from decorators import login_required
app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
# with app.app_context():
#     db.create_all()
# #登陆限制的装饰器
#
# #发布问答模块
@app.route('/question/',methods={'GET','POST'})
@login_required
def question():
    if request.method=='GET':
        return render_template('quetion.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        if title and content:

            question=Question(title=title,content=content)
            # user_id=session.get('user_id')
            # user=User.query.filter(User.id==user_id).first()
            question.author=g.user
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return '标题和文章不能为空'
#用户详情页
@app.route('/userdetail/')
def uesrdetail():
    return render_template('userdetail.html',user=g.user)
#详情页
@app.route('/detail/<question_id>')
def detail(question_id):
    detail_question=Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=detail_question)
#评论
@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('answer')
    question_id=request.form.get('question_id')
    answer=Answer(content=content)
    user_id=session['user_id']
    # user=User.query.filter(User.id==user_id).first()
    answer.author_id=user_id
    question=Question.query.filter(Question.id==question_id).first()
    answer.question=question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))
#钩子函数
@app.before_request
def before_request():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            g.user=user
#查找功能
@app.route('/search/')
def search():
    q=request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
    print(questions)
    if questions:
        return render_template('index.html',questions=questions)
    else:
        return render_template('search404.html')
@app.route('/')
def index():
    content={#order_by按什么排序 -表示时间顺序反过来321
        'questions':Question.query.order_by('-create_time').all()

    }
    return render_template('index.html',**content)
@app.route('/login/',methods={'GET','POST'})
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        telephone=request.form.get('telephone')
        password=request.form.get('password')
        user=User.query.filter(User.telephone==telephone).first()
        if user and user.check_password(password):#把用户的密码传过去加密比较，一致返回true否则密码错误
            session['user_id']=user.id
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return '密码或者用户名错误'
@app.route('/register/',methods={'GET','POST'})
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        #手机号码验证
        user=User.query.filter(User.telephone==telephone).first()
        if user:
            return "<script>alert('该手机号码已经被注册')</script>"
        else:
            if password1!=password2:
                return '两次密码输入不正确'
            else:
                user=User(telephone=telephone,username=username,pasdsword=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))
#登陆上下文处理
@app.context_processor
def my_context_processor():
        # user_id=session.get('user_id')
        # if user_id:
        #     user=User.query.filter(User.id==user_id).first()
        #     if user:
        #        return {'user':user}
        # return {}
        if hasattr(g,'user'):
            return {'user':g.user}
        return {}
#注销登陆功能
@app.route('/logout/')
def logout():
    #三种方式
    #session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))
if __name__ == '__main__':
    app.run()