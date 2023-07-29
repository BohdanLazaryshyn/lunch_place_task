# Lunch Decision Backend
This project was created to choose a restaurant for employees to hold lunch. The system allows employees to vote for a specific menu item in a specific restaurant to facilitate the decision making process. The server will be responsible for user registration and authentication, restaurant and menu management, employee registration, and will also provide information about the current day's menu and voting results.
***
## Technologies
Django + DRF, JWT, PostgreSQL, Docker(docker-compose), PyTests;
***
## Installation
```bash
$ git clone https://github.com/BohdanLazaryshyn/lunch_place_task.git
$ cd lunch_place_task

python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)

pip install -r requirements.txt

Your settings for DB in .env file:
POSTGRES_DB=<POSTGRES_DB>
POSTGRES_USER=<POSTGRES_USER>
POSTGRES_PASSWORD=<POSTGRES_PASSWORD>
POSTGRES_HOST=<POSTGRES_HOST>
SECRET_KEY=<YOUR DJANGO SECRET_KEY>

python manage.py migrate
python manage.py runserver
```
***
## Run Docker
```bash
$ docker-compose up --build
```
***
## Features
* User registration and authentication
* Restaurant and menu management
* Employee registration
* Information about the current day's menu and voting results
* Voting for a menu item in a specific restaurant
* Voting results