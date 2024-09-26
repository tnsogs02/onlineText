FROM python:3.12.6-slim-bookworm

WORKDIR /project

ADD . /project

RUN pip install numpy==1.26.4 flask pandas fasttext-wheel jieba pygsheets

CMD ["python", "./start.py"]