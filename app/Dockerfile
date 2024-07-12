# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose the port the app runs on (Streamlit is 8501)
EXPOSE 8501

# Command to run the app
CMD ["streamlit", "run", "home.py", "--server.port=8502", "--server.address=0.0.0.0"]
