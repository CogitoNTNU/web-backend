# Cogito-Website Backend

Backend for [Cogito-NTNU](https://cogito-ntnu.no)

![GitHub Django Workflow](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/web-backend/django.yml)
---

The backend is running on an aws ec2 server. To actually update the backend you need access to it.
If any changes are wished upon, contact Simon Sandvik Lee on Slack.

Caution: If you have a new feature you want to implement, do it on a branch!

Developed by [sandviklee](https://www.github/sandviklee)

## Docker

For ease of use and version management control, we use Docker to keep track of our containers and virtual environments.

#### Our Project

Our project uses docker to run the PostgreSQL server (database) and the Django Server.

#### Download Docker

To use docker, download docker engine [here](https://www.docker.com/get-started/)

#### How to run the Backend

To run the backend write the following commands in the terminal

To build the project:

```bash
docker-compose build
```

To run the project:

```bash
docker-compose up
```

#### Migrate the DB

To migrate django to the database

```bash
docker-compose run cogito python manage.py migrate
```

#### Create superuser

To log into the django database, create a superuser

```bash
docker-compose run cogito python manage.py createsuperuser
```

And follow the steps it gives you.

#### Finish!

Now you can access the django server through

```bash
http://127.0.0.1:8000/admin/
```
