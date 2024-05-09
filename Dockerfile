FROM python:3.12

ENV APP_HOME /ChatBot

RUN pip install poetry

WORKDIR $APP_HOME

COPY . .

RUN poetry install --no-root

EXPOSE 5000
ENTRYPOINT ["python", "main.py"]
