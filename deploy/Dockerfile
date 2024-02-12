# Python version
FROM python:3.10-slim
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV DATABASE_URL postgresql://docker:postgres@localhost:5432/listings_db
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_USER=docker
# Install system dependencies
RUN apt-get update && apt-get install -y postgresql postgresql-contrib
COPY ./app.py /deploy/
COPY ./setup_db.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./templates /deploy/templates
COPY ./static /deploy/static
COPY ./resources /deploy/resources
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
USER postgres
ENTRYPOINT service postgresql start &&\
    psql --command "CREATE USER docker WITH SUPERUSER PASSWORD 'postgres';" &&\
    python setup_db.py &&\
    gunicorn --workers 3 --bind 0.0.0.0:80 app:app --daemon
