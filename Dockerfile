# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Collect static files (if you are using Django's staticfiles)
RUN python manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Set the command to run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]