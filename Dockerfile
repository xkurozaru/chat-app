FROM python:3.9-alpine

RUN apk add git g++ musl-dev
RUN git clone https://github.com/xkurozaru/pbl_share.git myapp

WORKDIR myapp

RUN pip install flask flask-sqlalchemy

ENV FLASK_APP app.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]