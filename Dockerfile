FROM python:3.10
ENV PYTHONUNBUFFERED 1

COPY start /usr/local/bin/
RUN chmod +x /usr/local/bin/start
RUN ln -s /usr/local/bin/start /bin/start

RUN mkdir /book-manager
COPY . /book-manager/
WORKDIR /book-manager

RUN pip install -U pip
RUN pip install -r requirements.txt

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]