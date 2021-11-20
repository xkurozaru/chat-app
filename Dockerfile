FROM python:3.9-slim

RUN apt-get update
RUN apt-get install -y git
RUN apt install -y fonts-ipafont
RUN git clone https://github.com/xkurozaru/pbl_share.git myapp

WORKDIR myapp

RUN pip install flask flask-sqlalchemy
RUN pip install mecab-python3 ipadic
RUN pip install wordcloud

CMD ["python", "app.py"]
