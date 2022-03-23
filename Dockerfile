FROM python

COPY requirements.txt /opt/requirements.txt
RUN pip install -r /opt/requirements.txt

CMD ["python3", "/opt/main.py"]
COPY utils.py /opt/utils.py
COPY config.py /opt/config.py
COPY main.py /opt/main.py
