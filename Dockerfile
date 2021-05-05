FROM python:3
COPY check_conda_for_rc.py /check_conda_for_rc.py
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["/check_conda_for_rc.py"]
