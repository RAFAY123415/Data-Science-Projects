# Use an official Python runtime as the base image
FROM python:3.10.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt into the container at /app
COPY requirements.txt /app/

# Install any dependencies in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application into the container at /app
COPY . /app/

# Expose port 8000 (the default Gradio port)
EXPOSE 8000

# Command to run the application
CMD ["python", "Gradio_App.py"]
