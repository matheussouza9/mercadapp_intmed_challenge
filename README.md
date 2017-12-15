# mercadapp_intmed_challenge
This MVP application provides endpoints for mercadapp mobile app

## Prerequisites

* Python 3.5+
    * pip
* Django 2.0+
* Django Rest Framework 3.7.3+

## Installing and running

First, you need to clone the repository to the target machine. After it, enter in root project. 

```bash
$ git clone https://github.com/matheussouza9/mercadapp_intmed_challenge.git; cd mercadapp_intmed_challenge;
```

Now, you need to install all dependencies using pip

```bash
$ pip install -r requirements.txt
```

Create database structure

```bash
$ ./manage.py migrate
```

Create a super user for django admin

```bash
$ ./manage.py createsuperuser
```

Then, it's ready to run! Now, execute:

```bash
$ ./manage.py runserver
```

## Authors

* **Matheus Souza** - [msouzac](https://www.linkedin.com/in/msouzac)