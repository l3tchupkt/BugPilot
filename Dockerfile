FROM python:3.10-slim

# Install necessary pentesting and system tools
RUN apt-get update && apt-get install -y \
    nmap \
    curl \
    git \
    wget \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Install BugPilot globally
RUN pip install -e .

# Create directory for persistent data
RUN mkdir -p /root/.bugpilot/skills

# Default command
CMD ["bugpilot"]
