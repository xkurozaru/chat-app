from flask import *
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
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
    con = sqlite3.connect('chat.db')
    cur = con.cursor()
    cur.execute(
        "select id from user where username = username and password = password")
    id = cur.fetchone()[0]
    con.close
    if id is None:
        return redirect("/login")
    else:
        session["user_id"] = id
        return redirect("/mypage")
        
@app.route("/mypage")
def mypage():
    id = session['user_id']
    con = sqlite3.connect('chat.db')
    cur = con.cursor()
    cur.execute(
        "select username from user where id = id")
    username = cur.fetchone()[0]
    con.close
    chats = Chat.query.\
        filter(Chat.username==username).\
        all()
    return render_template("mypage.html", username=username, chats=chats)
    
@app.route("/send", methods=["POST"])
def send():
    date = str(datetime.datetime.now())
    message = request.form.get("message")
    id = session['user_id']
    username = User.query.\
        filter(Chat.id==id).\
        all()
    new_chat = Chat(username=username,date=date,message=message)
    db.session.add(new_chat)
    db.session.commit()
    return redirect('/mypage')

if __name__ == '__main__':
    app.run(debug=True)