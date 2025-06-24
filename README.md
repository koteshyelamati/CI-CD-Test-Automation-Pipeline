# Python Microservice CI/CD Pipeline Demo

This project demonstrates a complete CI/CD test automation pipeline for a Python microservice. It showcases the integration of GitHub Actions, Jenkins, Docker, and PyTest, along with code coverage, Slack alerts (placeholders), and deployment (placeholder).

[![CI Pipeline Status](https://github.com/koteshyelamati/CI-CD-Test-Automation-Pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/koteshyelamati/CI-CD-Test-Automation-Pipeline/actions/workflows/ci.yml)

## 🚀 Project Overview

A minimal Python microservice built with Flask, exposing two simple endpoints:
- `/health`: Returns a health status of the service.
- `/mock-data`: Returns a sample JSON data response.

The project emphasizes clean, modular coding standards and testability.

## 📁 Project Structure

/
├── .github/
│ └── workflows/
│ └── ci.yml
├── app/
│ ├── init.py
│ └── main.py
├── jenkins/
│ └── Dockerfile-jenkins
├── tests/
│ ├── init.py
│ └── test_app.py
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
└── README.md

markdown
Copy code

## 🏗️ Architecture

- Flask microservice (`app/main.py`)
- Unit + functional tests with PyTest (`tests/test_app.py`)
- CI/CD:
  - GitHub Actions for build/test on PRs
  - Jenkins with Docker integration for staging tests
- Reporting: HTML, coverage, JUnit XML

## 🛠️ CI/CD Workflows

### GitHub Actions
- Trigger: PRs and pushes to `main`
- Runs PyTest, generates reports, uploads artifacts

### Jenkins
- Jenkinsfile pipeline:
  - Docker build
  - Run tests in container
  - Archive reports

## 💻 Local Development

### Clone and Setup
```bash
git clone https://github.com/koteshyelamati/CI-CD-Test-Automation-Pipeline.git
cd CI-CD-Test-Automation-Pipeline
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app/main.py
Visit: http://localhost:5000/health

Run with Docker
bash
Copy code
docker-compose up --build app
Run Tests
bash
Copy code
pytest --cov=app --cov-report=term-missing --html=pytest-report.html --self-contained-html tests/
🧱 Jenkins Setup
bash
Copy code
docker-compose up --build jenkins
Open Jenkins at: http://localhost:8080
Find admin password in logs:

bash
Copy code
docker-compose logs jenkins | grep "Jenkins initial admin password"
🔔 Slack & Deployment (Optional)