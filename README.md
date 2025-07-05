# Cogito-Website Backend

<div align="center">

![GitHub Django Workflow](https://img.shields.io/github/actions/workflow/status/CogitoNTNU/web-backend/django.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>


Backend for [Cogito-NTNU](https://cogito-ntnu.no)
The backend is running on an aws ec2 server. To actually update the backend you need access to it.
If any changes are wished upon, contact Simon Sandvik Lee on Slack.

Caution: If you have a new feature you want to implement, do it on a branch!

Developed by [sandviklee](https://www.github/sandviklee)

## Docker

For ease of use and version management control, we use Docker to keep track of our containers and virtual environments.

#### Our Project

Our project uses docker to run the PostgreSQL server (database) and the Django Server.


## Quick Start
### Prerequisites
- Ensure that git is installed on your machine. [Download Git](https://git-scm.com/downloads)
- Docker is used for the backend and database setup. [Download Docker](https://www.docker.com/products/docker-desktop)

### Configuration
Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
DJANGO_SECRET_KEY = 'YOUR_SECRET_KEY'
EMAIL_HOST_USER = "YOUR_EMAIL"
EMAIL_HOST_PASSWORD  = "YOUR_EMAIL_PASSWORD"
```

Optionally, you can add the following environment variables to customize the project:

```bash
DEBUG = True
LOG_LEVEL = 'DEBUG' # DEBUG, INFO, WARNING, ERROR, CRITICAL
```

### Pre-commit Hooks 🚦

We use pre-commit to enforce code style, linting and simple security checks before every commit.
1. Install hooks once
    ```bash
    pip install --upgrade pre-commit
    pre-commit install
    ```

2. Run on all files

    ```bash
    pre-commit run --all-files
    ```

## Usage
To run the project, execute the following command in the root directory:

```bash
docker compose up --build
```


Once the project is running, you can access the Django admin panel at the [admin page](http://127.0.0.1:8000/admin/)


To see the endpoint documentation, visit the [OpenAPI/Swagger page](http://127.0.0.1:8000/swagger/)

## 📖 Documentation
- [Docker](docs/manuals/docker.md)
- [Deployment](docs/deployment/connect_to_EC2.md)
- [Commands](docs/manuals/commands.md)
