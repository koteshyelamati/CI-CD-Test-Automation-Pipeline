# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container at /usr/src/app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
# Using --no-cache-dir to reduce layer size and --compile to precompile .py to .pyc
RUN pip install --no-cache-dir --compile -r requirements.txt

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP app/main.py
ENV FLASK_RUN_HOST 0.0.0.0
# Recommended: Use a production WSGI server like Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]

# Fallback for development if Gunicorn is not preferred for local quick tests:
# CMD ["flask", "run"]
