# Book manager

## Setup with docker

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/nargessalehi98/book-manager
$ cd book-manager
```


```sh
$ docker build -t book-manager .
$ docker compose up
```

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
$ chmod u+x test.sh
$ ./test.sh

```


## Celery log

To see celery log, `cd` into the directory where `manage.py` is:
```sh
$ chmod u+x celery_run.sh
$ ./celery_run.sh

```