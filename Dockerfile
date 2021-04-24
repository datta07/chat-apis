FROM python:3.6.1-alpine
WORKDIR /Chat-APIS
ADD . /Chat-APIS
RUN pip install -r requirements.txt
CMD ["python","app.py"]