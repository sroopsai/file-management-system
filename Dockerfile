FROM python:3.9-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY ./server.py ./server.py
COPY ./commandhandler.py ./commandhandler.py
# Exposes at port 8088
EXPOSE 8088
CMD ["python3", "server.py"] 


