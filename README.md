# django-quiz

[![Python Version](https://img.shields.io/badge/python-3.6-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-2.0-brightgreen.svg)](https://djangoproject.com)

![home page](https://cdn1.savepice.ru/uploads/2018/10/1/0c409bb3b12198c244d2aa273c689398-full.png)
![test page](https://cdn1.savepice.ru/uploads/2018/10/1/363cc39895b87ca882a7da71a3ecc0c3-full.png)
![question page](https://cdn1.savepice.ru/uploads/2018/10/1/d5a47c79219fed048b5078abb58fc776-full.png)

## Running the Project Locally

First, clone the repository to your local machine:

```bash
git clone https://github.com/nkuznetsova/django-quiz.git
```

Install the requirements:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python manage.py migrate
```

Finally, run the development server:

```bash
python manage.py runserver
```

The project will be available at **127.0.0.1:8000**.
