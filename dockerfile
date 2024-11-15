# Use a Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file containing the dependencies
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all the source code into the container
COPY . .

# Expose the port on which Flask will run
EXPOSE 8080

# Start the Flask application
CMD ["python", "app.py"]
