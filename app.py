from enum import unique
from flask import *
import sqlite3
from flask_sqlalchemy import *
import datetime
import random

app = Flask(__name__)
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    date = db.Column(db.String(20))
    message = db.Column(db.String(400))

@app.route("/")
def tologin():
    return redirect ('/login')

@app.route("/login")
def login():
    return render_template("login.html", notification="Enter username and password.")

@app.route("/logincheck", methods=["POST"])
def logincheck():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter(User.username==username).filter(User.password==password).first()
    print(username)
    print(password)
    print(user)
    if user is None:
        return render_template("login.html", notification="Username or password is incorrect.")
    else:
        session["user_id"] = user.id
        return redirect("/timeline")

@app.route("/regist", methods=["POST"])
def regist():
    username = request.form.get('username')
    password = request.form.get('password')
    id = random.randint(1,99999999)
    print(username)
    print(password)
    print(id)

    if username=="" or password=="":
        return render_template("login.html", notification="Both username and password are needed.")
    
    if User.query.filter(User.username==username).first() is None:
        new_user = User(id=id,username=username,password=password)
        db.session.add(new_user)
        db.session.commit()
        return render_template("login.html", notification="Hello "+username+"!")
    else:
        return render_template("login.html", notification="This username is already used.")

@app.route("/mypage")
def mypage():
    id = session['user_id']
    username = User.query.filter(User.id==id).first().username
    chats = Chat.query.order_by(Chat.date.desc()).filter(Chat.username==username).all()
    return render_template("mypage.html", username=username, chats=chats)
    
@app.route("/send", methods=["POST"])
def send():
    id = session['user_id']
    date = str(datetime.datetime.now().replace(microsecond = 0))
    message = request.form.get('message')
    username = User.query.filter(User.id==id).first().username
    new_chat = Chat(username=username,date=date,message=message)
    db.session.add(new_chat)
    db.session.commit()
    return redirect('/mypage')

@app.route("/delete/<chatid>")
def delete(chatid):
    chat = Chat.query.get(chatid)
    db.session.delete(chat)
    db.session.commit()
    return redirect("/mypage")

@app.route("/timeline")
def timeline():
    id = session['user_id']
    username = User.query.filter(User.id==id).first().username
    chats = Chat.query.order_by(Chat.date.desc()).all()
    return render_template("timeline.html", username=username, chats=chats)

@app.route("/userpage/<username>")
def userpage(username):
    chats = Chat.query.order_by(Chat.date.desc()).filter(Chat.username==username).all()
    return render_template("userpage.html", username=username, chats=chats)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=os.environ['PORT'])