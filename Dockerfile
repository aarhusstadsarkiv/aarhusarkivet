FROM python:3.9-slim-bullseye
WORKDIR /usr/src/app
# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
#Server will reload itself on file changes if in dev mode
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "application.py"]
