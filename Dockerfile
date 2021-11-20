FROM python:3.9-slim

RUN apt update
RUN apt install -y git
RUN git clone https://github.com/xkurozaru/pbl_share.git myapp

WORKDIR myapp

RUN apt install -y fonts-ipafont
RUN apt install -y postgresql postgresql-contrib
RUN apt install -y python3-dev
RUN apt install -y gcc
RUN apt install -y libpq-dev

RUN pip install --upgrade pip
RUN pip install pytz
RUN pip install flask flask-sqlalchemy
RUN pip install psycopg2
RUN pip install mecab-python3 ipadic
RUN pip install wordcloud

RUN python database_init.py

CMD ["python", "app.py"]
