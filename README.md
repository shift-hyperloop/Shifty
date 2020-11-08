# Shifty

This project handles all the minor utility codes used by Shift Hyperloop

## Features

The main features of this project include:

- Checkin and checkout via RFID
- Kiosk

# Getting Started

## Prerequisites

To build this project you need:

- [python 3.x](https://www.python.org/download/releases/3.0/)
- [pip3](https://pip.pypa.io/en/stable/installing/)

Install the dependencies:

    $ pip install -r requirements.txt

## Installation

Clone the project:

    $ git clone git@github.com:shiftmro/Shifty.git

## Configuration / Environment

This project requires the following configuration / environment variables to run:

```
SHIFTY_MYSQL_USER=<MySQL Username>
SHIFTY_MYSQL_PASSWORD=<MySQL Password>
SHIFTY_MYSQL_DATABASE=<MySQL Database>
SHIFTY_MYSQL_HOST=<MySQL Host>
SHIFTY_MYSQL_PORT=<MySQL Port>
```

## Executing

Make sure you are in the folder Shifty/shifty and run the command:

    $ python manage.py runserver

# Main Dependencies

The main dependencies of this project are:

- [django](https://pypi.org/project/Django/)
- [mysqlclient](https://pypi.org/project/mysqlclient/)
