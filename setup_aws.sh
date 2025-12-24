#!/bin/bash

# AWS EC2 Setup Script for Jan Sevak (Ubuntu 22.04)
# Run this on your EC2 instance:
# chmod +x setup_aws.sh
# ./setup_aws.sh

set -e

echo "🚀 Starting AWS EC2 Setup..."

# 1. Update System
echo "📦 Updating System..."
sudo apt-get update
sudo apt-get upgrade -y

# 2. Install Dependencies
echo "📦 Installing Python, Nginx, Supervisor, Git..."
sudo apt-get install -y python3-pip python3-venv nginx supervisor git libpq-dev

# 3. Clone Repository (User needs to do this manually or provide repo URL)
# Assuming repo is cloned to /home/ubuntu/jan_sevak
PROJECT_DIR="/home/ubuntu/jan_sevak"
if [ ! -d "$PROJECT_DIR" ]; then
    echo "⚠️  Project directory $PROJECT_DIR not found."
    echo "    Please clone your repo first: git clone https://github.com/rupeshpoojary9/Jan-Sevak.git $PROJECT_DIR"
    exit 1
fi

# 4. Setup Virtual Environment
echo "🐍 Setting up Virtual Environment..."
cd $PROJECT_DIR
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 5. Collect Static Files
echo "🎨 Collecting Static Files..."
python3 manage.py collectstatic --noinput

# 6. Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/jan_sevak <<EOF
server {
    listen 80;
    server_name _;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }
    
    location /media/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/jan_sevak.sock;
    }
}
EOF

sudo ln -sf /etc/nginx/sites-available/jan_sevak /etc/nginx/sites-enabled
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# 7. Configure Supervisor
echo "👷 Configuring Supervisor..."
sudo tee /etc/supervisor/conf.d/jan_sevak.conf <<EOF
[program:jan_sevak]
user=ubuntu
directory=$PROJECT_DIR
command=$PROJECT_DIR/venv/bin/gunicorn --workers 3 --bind unix:$PROJECT_DIR/jan_sevak.sock jan_sevak.wsgi:application
autostart=true
autorestart=true
stderr_logfile=/var/log/jan_sevak.err.log
stdout_logfile=/var/log/jan_sevak.out.log
EOF

sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl restart jan_sevak

# 8. Setup Swap Memory (Crucial for t2.micro)
echo "💾 Setting up Swap Memory (1GB)..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 1G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
fi

echo "✅ Setup Complete! Your app should be live on your EC2 IP."
