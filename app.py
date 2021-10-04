from flask import *
import sqlite3
from flask_sqlalchemy import *
import datetime

app = Flask(__name__)
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    date = db.Column(db.String)
    message = db.Column(db.String)

@app.route("/")
def tologin():
    return redirect ('/login')

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/logincheck", methods=["POST"])
def logincheck():
    username = request.form.get("username")
    password = request.form.get("password")
    id = User.query.order_by().filter(User.username==username).filter(User.password==password).first()
    print(id)
    if id is None:
        return redirect("/login")
    else:
        session["user_id"] = id
        return redirect("/mypage")

@app.route("/regist", methods=["POST"])
def regist():
    username = request.form.get("username")
    password = request.form.get("password")
    User.username = username
    User.password = password
    db.session.add(User)
    db.session.commit()
    return redirect("/login")

@app.route("/mypage")
def mypage():
    id = session['user_id']
    username = User.query.order_by().filter(User.id==id).first()
    chats = Chat.query.order_by(Chat.date.desc()).filter(Chat.username==username).all()
    return render_template("mypage.html", username=username, chats=chats)
    
@app.route("/send", methods=["POST"])
def send():
    date = str(datetime.datetime.now().replace(microsecond = 0))
    message = request.form.get('message')
    id = session['user_id']
    username = User.query.order_by().filter(User.id==id).first()
    new_chat = Chat(username=username,date=date,message=message)
    db.session.add(new_chat)
    db.session.commit()
    return redirect('/mypage')

@app.route("/mainpage")
def mainpage():
    id = session['user_id']
    username = User.query.order_by().filter(User.id==id).first()
    chats = Chat.query.order_by(Chat.date.desc()).all()
    return render_template("mainpage.html", username=username, chats=chats)

@app.route("/userpage/<username>")
def userpage(username):
    chats = Chat.query.order_by(Chat.date.desc()).filter(Chat.username==username).all()
    return render_template("userpage.html", username=username, chats=chats)

if __name__ == '__main__':
    app.run(debug=True)