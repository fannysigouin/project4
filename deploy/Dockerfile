FROM python:3.10-slim
COPY ./app.py /deploy/
COPY ./requirements.txt /deploy/
COPY ./templates /deploy/templates
COPY ./static /deploy/static
COPY ./resources /deploy/resources
WORKDIR /deploy/
RUN pip install -r requirements.txt
EXPOSE 80
ENTRYPOINT ["python", "app.py"]
