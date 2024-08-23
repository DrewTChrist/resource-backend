# resource-backend
Backend built with FastAPI.


# Installation

## Dependencies
* python 3.10
* docker/docker-compose
* redis-server
* postgresql

## Docker

## Environment Variables

```shell
# connection string to db
DB_URL=""

# jwt signature for creating tokens
JWT_SIGNATURE=""

# asset directory
RESOURCE_DIRECTORY=""

# message broker url
CELERY_BROKER_URL=""

# message broker result backend url
CELERY_RESULT_BACKEND=""
```

Generate a new jwt signature key
```shell
openssl rand -hex 32
```

# Usage

