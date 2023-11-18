# MELP Backend

Backend for MELP

---
## Docker 

Provide permissions to files for the current user if not before running docker compose command.

```
sudo chown -R $USER:$USER .
```

Force build docker using command

```
docker compose -f "docker-compose.yml" up -d --build
```

Other docker commands

```
docker compose up   # run containers
docker ps           # list containers
docker compose down # shutdown containers
```

Executing django commands in docker container

```
docker exec -t melp_web python manage.py makemigrations 
docker exec -t melp_web python manage.py migrate 
docker exec -t melp_web python manage.py createsuperuser 
```

## Local setup

Running in local system by creating a seperate virtual environment for the project 

Install [virtualenv](https://pypi.org/project/virtualenv/): 

```
python -m pip install virtualenv
```

Create virtual environment for the project

```
virtualenv venv
```

Activate virtual environment venv

```
# for mac and linux
source venv/bin/activate

# for windows
.\venv\Scripts\activate
```

Install requirements for the project

```
pip install -r requirements.txt
```

Prepare django database

```
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

Run the Django server
```
python manage.py runserver
```
