FROM python:3.9-alpine

RUN apk add git g++ musl-dev
RUN apk add font-ipafont-gothic
RUN git clone https://github.com/xkurozaru/pbl_share.git myapp

WORKDIR myapp

#flask
RUN pip install flask flask-sqlalchemy

#Mecab
RUN apk add mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8


CMD ["python", "app.py"]
