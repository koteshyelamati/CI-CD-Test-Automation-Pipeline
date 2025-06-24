Overview:
This project showcases how to build a fully automated CI/CD pipeline for a Python-based microservice. I used GitHub Actions for test automation and integrated it with Jenkins for parallel execution. The app is containerized using Docker, and PyTest handles all unit and functional testing.

What I Did:

Created a Flask microservice with health check and mock data endpoints

Wrote PyTest test cases and tracked coverage using Codecov

Set up GitHub Actions to run tests on every pull request

Integrated Jenkins (via Docker) to support additional CI/CD stages

Configured Slack notifications for build and test results

