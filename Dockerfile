FROM python:3.9-alpine

RUN apk add git g++ musl-dev
RUN git clone https://github.com/xkurozaru/pbl_share.git myapp

WORKDIR myapp

RUN pip install --upgrade pip setuptools
RUN pip install flask flask-sqlalchemy
RUN pip install mecab-python3 ipadic
RUN pip install wordcloud
RUN apk add font-ipafont-gothic

CMD ["python", "app.py"]
