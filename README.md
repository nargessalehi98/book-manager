# Book manager

## Setup with virtual environment

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/nargessalehi98/book-manager
$ cd book-manager
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver 80
```
And navigate to `http://127.0.0.1:80/admin/`.


## Setup with docker

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/nargessalehi98/book-manager
$ cd book-manager
```

Create app image and run the container using given command:

```sh
$ docker build -t book-manager .
$ chmod u+x docker_run.sh
$ ./docker_run.sh
```

## Celery logs

...

## Tests

To run the tests, `cd` into the directory where `manage.py` is:
```sh
(env)$ python manage.py test 
```