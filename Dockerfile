FROM python:latest

ADD import_tasks.py /import_tasks.py

EXPOSE 4200

RUN pip install requests

CMD tail -f /dev/null