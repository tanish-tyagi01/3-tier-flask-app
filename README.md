# 3-Tier Flask Todo App

A containerized Todo application built with **Flask, MySQL, Gunicorn, Nginx, and Docker Compose**. The application demonstrates a simple production-style architecture where Nginx acts as a reverse proxy and Flask runs behind Gunicorn.

## Architecture

```text
                    Internet
                       │
                       │ HTTP :80
                       ▼
                ┌──────────────┐
                │    Nginx     │
                │ Reverse Proxy│
                └──────┬───────┘
                       │
                       │ :8000
                       ▼
                ┌──────────────┐
                │   Gunicorn   │
                │    Flask     │
                └──────┬───────┘
                       │
                       │ :3306
                       ▼
                ┌──────────────┐
                │    MySQL     │
                │  Persistent  │
                │    Volume    │
                └──────────────┘
```

Only Nginx is exposed to the host. Flask/Gunicorn and MySQL communicate through the internal Docker network.

## Tech Stack

* **Python / Flask** — Web application
* **Gunicorn** — WSGI application server
* **MySQL 8.0** — Database
* **Nginx** — Reverse proxy
* **Docker** — Containerization
* **Docker Compose** — Multi-container orchestration
* **Git & GitHub** — Version control
* **AWS EC2** — Cloud deployment

## Features

* User registration and login
* User-specific Todo tasks
* Create Todo
* Update Todo
* Delete Todo
* MySQL database persistence
* Containerized application
* Nginx reverse proxy
* Gunicorn application server
* Docker networking
* Persistent MySQL storage
* AWS EC2 deployment

## Project Structure

```text
3-tier-flask-app/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yaml
├── .env
├── .gitignore
│
└── nginx/
    └── nginx.conf
```

> Do not commit `.env` files containing passwords or other secrets.

## Docker Architecture

The application runs as multiple containers:

```text
todo-nginx
     │
     │ Docker Network
     ▼
flask-app
     │
     │ Docker Network
     ▼
mysql
```

### Nginx

Nginx listens on port `80` and forwards incoming requests to the Flask application.

Example:

```nginx
location / {
    proxy_pass http://flask-app:8000;

    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Flask + Gunicorn

Gunicorn runs the Flask application on port `8000`:

```bash
gunicorn --bind 0.0.0.0:8000 app:app
```

Flask's port is kept internal to the Docker network because Nginx is the public entry point.

### MySQL

MySQL runs on port `3306` inside the Docker network.

Database data is stored using a persistent Docker volume so that removing/recreating the MySQL container does not automatically remove the database data.

## Running the Application

### 1. Clone the repository

```bash
git clone https://github.com/tanish-tyagi01/3-tier-flask-app.git
cd 3-tier-flask-app
```

### 2. Configure environment variables

Create a `.env` file:

```env
MYSQL_ROOT_PASSWORD=your_password
MYSQL_DATABASE=devops
```

Use your actual application/database variables according to the Compose configuration.

### 3. Build and start the containers

```bash
docker compose up -d --build
```

### 4. Check running containers

```bash
docker compose ps
```

Expected architecture:

```text
nginx       → port 80
flask-app   → internal port 8000
mysql       → internal port 3306
```

### 5. Access the application

Open:

```text
http://<EC2-PUBLIC-IP>/
```

Nginx receives the request and forwards it to Flask/Gunicorn.

## Useful Docker Commands

### View running containers

```bash
docker compose ps
```

### View logs

```bash
docker compose logs
```

For a specific service:

```bash
docker logs todo-nginx
docker logs flask-app
docker logs mysql
```

### Follow logs

```bash
docker logs -f todo-nginx
```

### Stop the application

```bash
docker compose down
```

### Rebuild the application

```bash
docker compose up -d --build
```

### Check Docker networks

```bash
docker network ls
```

### Inspect a container

```bash
docker inspect flask-app
```

## Troubleshooting

### 502 Bad Gateway

Check:

```bash
docker compose ps
docker logs todo-nginx
docker logs flask-app
```

Verify that Nginx is forwarding to the correct Docker service:

```nginx
proxy_pass http://flask-app:8000;
```

Also verify that Gunicorn is listening on:

```text
0.0.0.0:8000
```

### Nginx cannot resolve Flask

Check Docker DNS from the Nginx container:

```bash
docker exec todo-nginx getent hosts flask-app
```

The Flask container and Nginx container must be connected to the same Docker network.

### Database connection problems

Check:

```bash
docker logs mysql
docker logs flask-app
```

Make sure the Flask application uses the Docker Compose service name:

```text
mysql
```

rather than:

```text
localhost
```

inside the container.

## AWS EC2 Deployment

The application can be deployed on an AWS EC2 instance using Docker Compose.

High-level deployment flow:

```text
GitHub
   │
   ▼
AWS EC2
   │
   ▼
Docker Compose
   │
   ├── Nginx
   ├── Flask + Gunicorn
   └── MySQL
```

The EC2 Security Group should allow HTTP traffic on port `80`.

Application ports `8000` and `3306` do not need to be publicly exposed because communication between the services happens through the Docker network.

## Security Considerations

* Do not commit database passwords to GitHub.
* Store secrets in environment variables or a secret-management system.
* Expose only required ports.
* Keep MySQL inaccessible from the public internet.
* Keep the Flask/Gunicorn application behind Nginx.
* Use HTTPS for a production deployment.

## Future Improvements

* GitHub Actions CI/CD
* Docker image publishing to Docker Hub
* Automated deployment to EC2
* HTTPS with Let's Encrypt
* AWS Application Load Balancer
* CloudWatch monitoring
* Automated database backups
* Infrastructure as Code using Terraform

## What This Project Demonstrates

This project demonstrates practical experience with:

* Linux
* Docker
* Docker Compose
* Container networking
* Persistent storage
* Flask
* Gunicorn
* Nginx reverse proxy
* MySQL
* Git/GitHub
* AWS EC2
* Application troubleshooting

## Author

**Tanish Tyagi**

GitHub: `tanish-tyagi01`
