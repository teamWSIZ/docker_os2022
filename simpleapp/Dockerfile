#FROM python:3.10.9-slim-buster
FROM python:3.10.9-alpine3.17

# docker build -t wsiz/simpleapp:0.0.1 .

# Create app directory
WORKDIR /usr/src/app


# Bundle app source
COPY . /usr/src/app/
RUN pip install -r requirements.txt
EXPOSE 5005
CMD [ "python", "-u", "controller.py" ]
