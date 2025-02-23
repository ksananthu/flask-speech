# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/key /app/log
# Expose the port
EXPOSE 8080

# Use ENTRYPOINT for more control over command execution
ENTRYPOINT ["python", "app.py"]

# Pass host and port arguments explicitly
CMD ["--host=0.0.0.0", "--port=8080"]
