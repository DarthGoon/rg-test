FROM python:3.9.2

WORKDIR /opt

COPY app/ .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "/opt/server.py"]
