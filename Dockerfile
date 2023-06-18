FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED 1

RUN mkdir app_source
WORKDIR app_source

COPY ./requirements.txt .
RUN pip install -r requirements.txt