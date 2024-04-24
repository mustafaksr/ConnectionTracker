# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory within the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app/

# Set the environment variable to enable Flask's debug mode
# ENV FLASK_ENV=development

# Expose the port on which the Flask app will run
EXPOSE 2000

# Define the command to run the application when the container starts
CMD ["python", "app.py"]
