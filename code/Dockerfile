
FROM python:3.11-alpine3.18

COPY ./webapp.py /app/

COPY ./Pipfile /app/

WORKDIR /app/

RUN pip install pipenv

RUN pipenv install 

EXPOSE 8080

CMD pipenv run python3.11 webapp.py

