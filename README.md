# Python Microservice CI/CD Pipeline Demo

This project demonstrates a complete CI/CD test automation pipeline for a Python microservice. It showcases the integration of GitHub Actions, Jenkins, Docker, and PyTest, along with code coverage, Slack alerts (placeholders), and deployment (placeholder).

[![CI Pipeline Status](https://github.com/YOUR_USERNAME/YOUR_REPONAME/actions/workflows/ci.yml/badge.svg)](https://github.com/YOUR_USERNAME/YOUR_REPONAME/actions/workflows/ci.yml)
<!-- Replace YOUR_USERNAME and YOUR_REPONAME with your actual GitHub username and repository name -->
<!-- Add Codecov badge after setting up Codecov.io:
[![codecov](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPONAME/branch/main/graph/badge.svg?token=YOUR_CODECOV_TOKEN)](https://codecov.io/gh/YOUR_USERNAME/YOUR_REPONAME)
-->

## Project Overview

A minimal Python microservice built with Flask, exposing two simple endpoints:
*   `/health`: Returns a health status of the service.
*   `/mock-data`: Returns a sample JSON data response.

The project emphasizes clean, modular coding standards and testability.

## Project Structure

```
/
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI workflow
├── app/                     # Source code for the Flask microservice
│   ├── __init__.py
│   └── main.py
├── jenkins/
│   └── Dockerfile-jenkins   # Dockerfile for custom Jenkins image with Docker CLI
├── tests/                   # PyTest-based unit & functional tests
│   ├── __init__.py
│   └── test_app.py
├── .dockerignore            # Specifies intentionally untracked files for Docker
├── Dockerfile               # Containerizes the microservice
├── docker-compose.yml       # For running the app + Jenkins locally
├── Jenkinsfile              # Jenkins pipeline definition
├── requirements.txt         # Python dependencies
└── README.md                # This file
```

## Architecture Overview

*   **Microservice**: A simple Flask application (`app/main.py`) serves API endpoints.
*   **Testing**: PyTest (`tests/test_app.py`) is used for unit and functional testing. Code coverage is measured using `pytest-cov`.
*   **Containerization**: Docker (`Dockerfile`) is used to package the microservice. Docker Compose (`docker-compose.yml`) facilitates local development and running a local Jenkins instance.
*   **CI/CD**:
    *   **GitHub Actions**: Triggered on pushes and pull requests to the `main` branch. It installs dependencies, runs tests across multiple Python versions, uploads test/coverage reports (Codecov), and generates a summary.
    *   **Jenkins**: A `Jenkinsfile` defines a pipeline that checks out code, builds the Docker image for the microservice, runs tests within that Docker image, and archives test/coverage reports. The Jenkins setup itself is also containerized and includes Docker CLI for these operations.

## CI/CD Flow

### 1. GitHub Actions (`.github/workflows/ci.yml`)

*   **Trigger**: On `push` or `pull_request` to the `main` branch.
*   **Jobs**:
    *   `build-and-test`:
        1.  **Checkout**: Checks out the repository code.
        2.  **Set up Python**: Configures specified Python versions (e.g., 3.9, 3.10, 3.11).
        3.  **Install Dependencies**: Installs packages from `requirements.txt`.
        4.  **Run Tests**: Executes PyTest, generates coverage reports (`coverage.xml`, `term-missing`), JUnit XML (`junit-report.xml`), and an HTML report (`pytest-report.html`).
        5.  **Upload to Codecov**: Uploads `coverage.xml` to Codecov.io for tracking coverage trends (requires `CODECOV_TOKEN` secret).
        6.  **Archive Reports**: Uploads `pytest-report.html` and `junit-report.xml` as build artifacts.
        7.  **Generate Summary**: Creates a job summary with test statistics.
        8.  **Slack Notifications (Placeholder)**: Send notifications on build status (requires `SLACK_WEBHOOK_URL` secret).

### 2. Jenkins Pipeline (`Jenkinsfile`)

*   **Trigger**: Typically configured in Jenkins UI to poll SCM (e.g., this GitHub repository) or triggered by a webhook from GitHub.
*   **Environment**: Uses a custom Jenkins Docker image (`jenkins/Dockerfile-jenkins`) which includes Docker CLI. The `docker-compose.yml` file can be used to run this Jenkins setup locally.
*   **Stages**:
    1.  **Checkout**: Checks out the source code from the SCM.
    2.  **Build Docker Image**: Builds the Docker image for the Python microservice using the `Dockerfile`.
    3.  **Run Tests in Docker**: Runs PyTest (with coverage and report generation) *inside* the newly built application Docker container. Test results (JUnit XML, HTML report, coverage XML) are written to a mounted volume in the Jenkins workspace.
    4.  **Archive & Display Results**:
        *   Archives JUnit XML for Jenkins to track test trends.
        *   Publishes the HTML test report for easy viewing.
        *   Archives the `coverage.xml` artifact.
    5.  **Upload Coverage to Codecov (Placeholder)**: Can be configured using the Codecov Jenkins plugin or a script step.
    6.  **Deploy to Test Server (Placeholder)**: Can be configured to deploy the application (e.g., to Heroku, AWS EC2) if tests pass.
    7.  **Slack Notifications (Placeholder)**: Send notifications on build status.
*   **Post Actions**:
    *   Cleans up the workspace.

## Local Setup and Execution

### Prerequisites

*   Git
*   Python 3.8+ and pip
*   Docker
*   Docker Compose

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPONAME.git
cd YOUR_REPONAME
```
<!-- Update with your repo URL -->

### 2. Running the Microservice Locally (Python Virtual Environment)

```bash
# Create and activate a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app/main.py
```
The service will be available at `http://localhost:5000`.
*   Health check: `http://localhost:5000/health`
*   Mock data: `http://localhost:5000/mock-data`

### 3. Running the Microservice Locally (Docker)

```bash
# Build and run the application container using Docker Compose
docker-compose up --build app
```
The service will be available at `http://localhost:5000`. To stop: `CTRL+C` then `docker-compose down`.

### 4. Running Tests Locally

Ensure you have installed dependencies (including `pytest`, `pytest-cov`, `pytest-html`).

```bash
# Activate virtual environment if you have one
# source venv/bin/activate

# Run pytest
pytest

# Run pytest with coverage and HTML report
pytest --cov=app --cov-report=term-missing --html=pytest-report.html --self-contained-html tests/
```
*   Coverage report will be printed to the console and also in `htmlcov/` if configured.
*   HTML test report will be generated as `pytest-report.html`.
*   JUnit XML report can be generated with `pytest --junitxml=report.xml tests/`.

### 5. Running Jenkins Locally with Docker Compose

This setup allows you to test the `Jenkinsfile` pipeline.

```bash
# Start the Jenkins service along with the app (optional for app)
docker-compose up --build jenkins
# If you only want jenkins: docker-compose up --build jenkins
```

1.  **Access Jenkins**: Open your browser and go to `http://localhost:8080` (or `http://localhost:8080/jenkins` if `JENKINS_OPTS="--prefix=/jenkins"` is active in `docker-compose.yml`).
2.  **Initial Setup (if not disabled by `JAVA_OPTS` in `docker-compose.yml`):**
    *   Jenkins will require an initial admin password. You can get this from the logs of the Jenkins container:
        ```bash
        docker-compose logs jenkins | grep "Jenkins initial admin password"
        ```
    *   Copy the password and paste it into the Jenkins setup wizard.
    *   Choose "Install suggested plugins."
    *   Create an admin user.
3.  **Create a New Jenkins Pipeline Job**:
    *   Click "New Item".
    *   Enter an item name (e.g., "python-microservice-pipeline").
    *   Select "Pipeline" and click "OK".
    *   **Configuration**:
        *   Scroll down to the "Pipeline" section.
        *   **Definition**: Choose "Pipeline script from SCM".
        *   **SCM**: Select "Git".
        *   **Repository URL**: Enter the URL of this GitHub repository (e.g., `https://github.com/YOUR_USERNAME/YOUR_REPONAME.git`).
            *   If your repository is private, you'll need to add credentials.
        *   **Branch Specifier**: Set to `*/main` (or your primary branch name).
        *   **Script Path**: Ensure it's `Jenkinsfile` (this is the default).
        *   Click "Save".
4.  **Run the Pipeline**:
    *   Click "Build Now" on the pipeline job page.
    *   You can view the console output to see the stages execute.

## Test Reports and Coverage

*   **GitHub Actions**:
    *   Test results (HTML, JUnit XML) are uploaded as artifacts for each run.
    *   Coverage reports are sent to Codecov.io (link will be in the README badge once set up).
    *   A summary of test results is added to the GitHub Actions run summary page.
*   **Jenkins**:
    *   Test results are displayed within Jenkins (trend graphs, HTML report via "Pytest HTML Report" link on the build page).
    *   `coverage.xml` is archived, which can be used with the Codecov plugin or downloaded.
*   **Local**:
    *   `pytest-report.html` provides a detailed HTML test report.
    *   Coverage data can be viewed in the console or via an HTML report generated by `coverage html` (after running `pytest --cov`).

## Slack Notifications (Setup Required)

Both GitHub Actions (`ci.yml`) and Jenkins (`Jenkinsfile`) have placeholder steps for Slack notifications. To enable them:

1.  **Create a Slack App** and an incoming webhook URL.
2.  **For GitHub Actions**:
    *   Add the webhook URL as a secret named `SLACK_WEBHOOK_URL` in your GitHub repository settings (`Settings > Secrets and variables > Actions`).
    *   Uncomment the Slack notification steps in `.github/workflows/ci.yml`.
3.  **For Jenkins**:
    *   Install the "Slack Notification" plugin in Jenkins (`Manage Jenkins > Plugins`).
    *   Configure the plugin with your Slack workspace and webhook URL/token.
    *   Store the webhook URL or token as a Jenkins credential (e.g., `SLACK_WEBHOOK_JENKINS`).
    *   Uncomment and configure the `slackSend` steps in the `post` section of the `Jenkinsfile`.

## Deployment (Placeholder - Heroku Example)

The pipelines include placeholder stages for deployment. Here's a conceptual example for Heroku:

### Prerequisites for Heroku Deployment

1.  **Heroku Account**: Sign up at [heroku.com](https://www.heroku.com/).
2.  **Heroku CLI**: Install it locally.
3.  **Create Heroku App**: `heroku create your-unique-app-name`
4.  **Set `HEROKU_API_KEY`**:
    *   Get your API key: `heroku authorizations:create` (or from your Heroku dashboard).
    *   **GitHub Actions**: Add it as a secret `HEROKU_API_KEY`.
    *   **Jenkins**: Add it as a secret text credential (e.g., `HEROKU_API_KEY_JENKINS`).
5.  **Set `HEROKU_APP_NAME`**:
    *   **GitHub Actions**: Add your Heroku app name as a secret `HEROKU_APP_NAME`.
    *   **Jenkins**: You can set this as an environment variable or directly in the deployment script.

### `Dockerfile` for Heroku

Heroku's container runtime uses the `web` process type defined in your `heroku.yml` or infers from `CMD`. Ensure your `Dockerfile`'s `CMD` is suitable for Heroku (e.g., using Gunicorn and binding to `$PORT`).

```dockerfile
# ... (rest of your Dockerfile) ...

# Heroku sets the PORT environment variable.
# Gunicorn should bind to 0.0.0.0 and use this $PORT.
CMD gunicorn --bind 0.0.0.0:$PORT app.main:app
```

### Deployment Step in GitHub Actions (Example)

```yaml
# In .github/workflows/ci.yml
# - name: Deploy to Heroku
#   if: github.ref == 'refs/heads/main' && success() # Only deploy main on success
#   env:
#     HEROKU_API_KEY: ${{ secrets.HEROKU_API_KEY }}
#     HEROKU_APP_NAME: ${{ secrets.HEROKU_APP_NAME }}
#   run: |
#     docker login --username=_ --password=$HEROKU_API_KEY registry.heroku.com
#     heroku container:push web --app $HEROKU_APP_NAME
#     heroku container:release web --app $HEROKU_APP_NAME
```

### Deployment Step in Jenkinsfile (Example)

```groovy
// In Jenkinsfile, within the deploy stage
// steps {
//     withCredentials([string(credentialsId: 'HEROKU_API_KEY_JENKINS', variable: 'HEROKU_API_KEY')]) {
//         sh """
//             echo "Logging into Heroku..."
//             echo "${HEROKU_API_KEY}" | docker login --username=_ --password-stdin registry.heroku.com
//             echo "Pushing to Heroku container registry..."
//             # Assuming DOCKER_IMAGE_NAME and DOCKER_IMAGE_TAG are set
//             # We might need to retag the image for Heroku:
//             # docker tag ${DOCKER_IMAGE_NAME}:${DOCKER_IMAGE_TAG} registry.heroku.com/${HEROKU_APP_NAME}/web
//             # heroku container:push web --app ${HEROKU_APP_NAME} # If using local Docker image directly

//             # More robust: Use the image built by Jenkins
//             docker tag ${env.DOCKER_IMAGE_NAME}:${env.DOCKER_IMAGE_TAG} registry.heroku.com/YOUR_HEROKU_APP_NAME/web
//             docker push registry.heroku.com/YOUR_HEROKU_APP_NAME/web

//             echo "Releasing application on Heroku..."
//             heroku container:release web --app YOUR_HEROKU_APP_NAME
//         """
//     }
// }
```
**Note**: The Heroku deployment steps above are illustrative. You'll need to adjust them for your specific Heroku app name and potentially how you tag/push images. `YOUR_HEROKU_APP_NAME` should be replaced.

## Future Enhancements / Optional Features

*   **Load Testing**: Integrate tools like K6 or Locust into a separate Jenkins pipeline.
*   **Smoke Tests**: Add a stage after deployment to run quick checks against the live environment.
*   **Security Scanning**: Incorporate tools like Snyk or Trivy to scan dependencies and Docker images.
*   **More Sophisticated Deployment**: Blue/green deployments, canary releases.
*   **Infrastructure as Code**: Use Terraform or CloudFormation if deploying to AWS.
*   **Semantic Versioning and Release Management**.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

*This README provides a comprehensive guide to understanding, setting up, and running the project. Remember to replace placeholder values (like `YOUR_USERNAME`, `YOUR_REPONAME`, `YOUR_CODECOV_TOKEN`, Heroku app names, etc.) with your actual details.*