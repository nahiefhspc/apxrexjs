# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (optional, for local testing)
EXPOSE 8080

# Command to run the application
CMD ["python3", "main.py"]
