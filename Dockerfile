FROM apache/airflow:2.6.1
ADD requirements.txt .
RUN pip install -r requirements.txt