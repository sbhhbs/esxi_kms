FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH=/root/app
WORKDIR /root/app
COPY main.py main.py
COPY gen_cert.py gen_cert.py
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
CMD ["python", "main.py"]