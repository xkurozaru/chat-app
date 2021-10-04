FROM python:3.9-alpine

RUN apk add git g++ musl-dev
RUN git clone https://https://github.com/xkurozaru/pbl_share /myapp

WORKDIR myapp

RUN pip install Flask
RUN pip install flask-sqlalchemy

ENV FLASK_APP app.py
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]