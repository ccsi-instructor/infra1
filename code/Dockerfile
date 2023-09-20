FROM python:3.11-alpine

COPY ./webapp.py /app/

COPY ./Pipfile /app/

WORKDIR /app/

RUN pip install pipenv

RUN pipenv install 

EXPOSE 80

CMD pipenv run python webapp.py

