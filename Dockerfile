FROM python:3.10
ENV PYTHONUNBUFFERED 1

RUN mkdir /book-manager
WORKDIR /book-manager

RUN pip install -U pip
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

COPY . /book-manager/

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]
