from enum import unique
from flask import *
import sqlite3
from flask_sqlalchemy import *
import psycopg2
import datetime
import random
import os
import MeCab
import ipadic
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from io import BytesIO

app = Flask(__name__)
app.secret_key = 'qwertyuiopasdfghjklzxcvbnm'
#os.environ['DATABASE_URL']
db_url = 'postgresql://rskhavvdgvymkn:d72f7e3139165ac0f583c795e5fc77b2dd6a4593599df41273ab5453eec5257b@ec2-54-145-9-12.compute-1.amazonaws.com:5432/devdftovtitgd'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
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

db.create_all()

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
    date = str(datetime.datetime.utcnow().replace(microsecond = 0) + datetime.timedelta(hours=9))
    message = request.form.get('message')
    username = User.query.filter(User.id==id).first().username
    new_chat = Chat(username=username,date=date,message=message)
    db.session.add(new_chat)
    db.session.commit()
    return redirect('/timeline')

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

@app.route("/trend/<period>")
def trend(period):
    now = datetime.datetime.now().replace(microsecond = 0) + datetime.timedelta(hours=9)

    tagger = MeCab.Tagger(ipadic.MECAB_ARGS)
    noun_list = []

    if(period=="all"):
        chats = Chat.query.order_by().all()
    elif(period=="day"):
        date_str = str(now.year) + "-" + str(now.month) + "-" + str(now.day)
        chats = Chat.query.order_by().filter(Chat.date.startswith(date_str)).all()
    elif(period=="month"):
        date_str = str(now.year) + "-" + str(now.month)
        chats = Chat.query.order_by().filter(Chat.date.startswith(date_str)).all()
    elif(period=="year"):
        date_str = str(now.year)
        chats = Chat.query.order_by().filter(Chat.date.startswith(date_str)).all()

    for chat in chats:
        node = tagger.parseToNode(chat.message)
        while node:
            feature = node.feature
            features = feature.split(',')
            hinshi = features[0]

            if hinshi != "名詞":
                node = node.next
            else:
                surface = node.surface
                noun_list.append(surface)
                node = node.next

    noun_string = ' '.join(noun_list)
    print(noun_string)
    wordcloud = WordCloud(
        font_path='/usr/share/fonts/opentype/ipag.ttf',
        width=900,
        height=600,
        background_color="white",
        max_words=500,min_font_size=4,
        collocations = False).generate(noun_string)

    fig = plt.figure(figsize=(15,12))
    plt.imshow(wordcloud)
    plt.axis("off")

    canvas = FigureCanvasAgg(fig)
    png_output = BytesIO()
    canvas.print_png(png_output)
    data = png_output.getvalue()
    response = make_response(data)
    response.headers['Content-Type'] = 'image/png'
    response.headers['Content-Length'] = len(data)
    return response

if __name__ == '__main__':
    #app.run(debug=True,port=5001)
    app.run(debug=True, host="0.0.0.0", port=os.environ['PORT'])
