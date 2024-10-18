FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install Nmap
RUN apt-get update && apt-get install -y nmap

# Copy the requirements file into the container
COPY requirements.txt .

# Upgrade the pip to the lastest
RUN pip install --upgrade pip

# TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO TODO