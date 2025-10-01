# SVJIS2

[![UnitTests](https://github.com/svjis/svjis2/actions/workflows/unit-tests.yml/badge.svg)](https://github.com/svjis/svjis2/actions/workflows/unit-tests.yml) [![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=svjis_svjis-py&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=svjis_svjis-py)

Information system for homeowners' associations (SVJ). :house_with_garden:

## Project Description

SVJIS is a CMS for Homeowners' Associations. The system provides a content management system :memo:, discussions under articles, polls :bar_chart:, reporting and tracking of issues, advertisements, and a database of owners :family_man_woman_boy: including records of units and shares. More on the [project website](https://svjis.github.io/Vlastnosti/).

## 1 Installation
It is assumed that you have Python version 3.10 or higher installed on your computer.

```
python --version
```

Clone the project
```
git clone https://github.com/svjis/svjis2.git
cd svjis2
```

Inatall `uv`
https://docs.astral.sh/uv/getting-started/installation/


Install the dependencies
```
uv sync
# in Linuxu
source .venv/bin/activate
# in Windows
source .venv/Scripts/activate
```

Create the configuration
```
cd svjis
python manage.py migrate
python manage.py svjis_setup --password <password for admin user>
```

> [!NOTE]
> To compile the translations, you will need to have the `gettext` utility installed - try `gettext --version`. If you don't have it, feel free to skip the next step, and the application will only be available in English.
```
python manage.py compilemessages
```

## 2 Starting application

```
python manage.py runserver
```

The application runs at the address http://127.0.0.1:8000/ with the user `admin` and the password is the one you entered earlier.

The method of starting mentioned is suitable for quickly testing the application on your computer or for developers. If you want to deploy SVJIS on a production server, please read the [Django documentation](https://docs.djangoproject.com/en/5.0/howto/deployment/).

On the project pages, you will find a step-by-step [example of installation on a server (Debian, Apache, Postgres)](https://svjis.github.io/Instalace/).

## 3 Parameterization

### 3.1 SVJ Data

The settings for SVJ data can be found in the application under the `Administration` section.

### 3.2 Email Sending Settings

The SVJIS system uses email sending for various events, so the correct configuration of the email interface is essential for the application's functionality.

Create a new file `svjis/svjis/local_settings.py` and add the following configuration:

```
SECRET_KEY = 'production django secret'
TIME_ZONE = 'Europe/Prague'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'your smtp server'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'username to your smtp server'
EMAIL_HOST_PASSWORD = 'password to your smtp server'
```

Email sending occurs in the background - the system stores emails in a queue for sending, see `Administration - pending messages`. To send messages, you need to run the following command:

```
python manage.py svjis_send_messages
```

During application testing, you can run it manually. In a production setup, you need to configure a system scheduler (like cron) to run it at certain intervals (for example, every 5 minutes).

## 4 Troubleshooting

If you encounter any issues, do not hesitate to ask a question in the [project discussions](https://github.com/orgs/svjis/discussions).

## 5 Collaboration

Any form of collaboration is welcome. :octocat:  
More information can be found in [CONTRIBUTING.md](CONTRIBUTING.md).
