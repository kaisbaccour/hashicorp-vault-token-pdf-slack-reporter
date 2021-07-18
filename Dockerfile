FROM python

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

COPY main.py /opt/main.py

CMD ["python3", "/opt/main.py"]