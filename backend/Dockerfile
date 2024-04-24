# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN apt-get update && \
    apt-get install -y libpq-dev
RUN pip install --no-cache-dir -r requirements.txt

# Make port 7050 available to the world outside this container
EXPOSE 7050

# Define environment variable for Flask
ENV FLASK_APP app.py

# Run the command to start the backend server
CMD ["flask", "run", "--host=0.0.0.0", "--port=7050"]
