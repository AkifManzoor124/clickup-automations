FROM python:latest

ADD import_tasks.py /import_tasks.py

RUN pip install requests

CMD ["python", "./import_tasks.py"]