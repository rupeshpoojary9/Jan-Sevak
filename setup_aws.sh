#!/bin/bash

# AWS EC2 Setup Script for Jan Sevak (Docker Version)
# Run this on your EC2 instance:
# chmod +x setup_aws.sh
# ./setup_aws.sh

set -e

echo "🚀 Starting AWS EC2 Setup (Docker Mode)..."

# 1. Update System
echo "📦 Updating System..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Docker & Docker Compose
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    sudo apt-get install -y ca-certificates curl gnupg
    sudo install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    sudo chmod a+r /etc/apt/keyrings/docker.gpg

    echo \
      "deb [arch="$(dpkg --print-architecture)" signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
      "$(. /etc/os-release && echo "$VERSION_CODENAME")" stable" | \
      sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    sudo apt-get update
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    echo "⚠️  Docker installed. You might need to log out and log back in for group changes to take effect."
else
    echo "✅ Docker already installed."
fi

# 3. Clone Repository (User needs to do this manually or provide repo URL)
PROJECT_DIR="/home/ubuntu/jan_sevak"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "⚠️  Project directory $PROJECT_DIR not found."
    echo "    Please clone your repo first: git clone https://github.com/rupeshpoojary9/Jan-Sevak.git $PROJECT_DIR"
    exit 1
fi

# 4. Setup Swap Memory (Crucial for t2.micro)
echo "💾 Setting up Swap Memory (1GB)..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

# 5. Deploy
echo "🚀 Deploying with Docker Compose..."
cd $PROJECT_DIR

# Check for .env
if [ ! -f .env ]; then
    echo "❌ .env file missing! Please create it before running this script."
    exit 1
fi

# Build and Run
sudo docker compose -f docker-compose.prod.yml up -d --build

echo "✅ Deployment Complete! Your app is running on Port 80."
echo "   Check logs with: docker compose -f docker-compose.prod.yml logs -f"
