# Project Description

This project implements a RESTful API service using Django, a powerful web framework for building web applications in Python. The service provides CRUD (Create, Read, Update, Delete) operations for Client entities and their corresponding Request entities. Additionally, there is an Operator entity responsible for updating the Status of the Request entity. The service utilizes Django's Object-Relational Mapping (ORM) for data modeling and interaction with the database.

## Local Deployment
To deploy the project locally, follow these instructions:

### Prerequisites

- Docker 
- Docker Compose

### Steps

1. Clone the repository:
```bash
git clone https://github.com/EdAlekseiev/helpdesk.git
cd helpdesk
```
2. Create a .env file in the project root directory with the following environment variables:
```bash
SECRET_KEY=SECRET_KEY
DEBUG=DEBUG # 1 or 0
DJANGO_ALLOWED_HOSTS=DJANGO_ALLOWED_HOSTS # localhost,127.0.0.1
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
```
3. Build and run the Docker containers:
```bash
docker-compose up --build
```
4. Access the API at http://localhost:8000/.
5. Swagger http://localhost:8000/swagger/.
6. Load fixtures with init data:
```bash
sudo docker exec -i <application container name> python manage.py loaddata fixtures/init_fixture.json
```

## Test User Credentials:
### Admin:
- Username: admin
- Password: 894769

### Client 1:
- Username: 0666666601
- Password: 894769

### Client 2:
- Username: 0666666602
- Password: 894769

### Operator:
- Username: test_operator
- Password: 894769
