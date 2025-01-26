#!/bin/bash

# --- Load environment variables ---
source ./.env

# --- Functions ---

# Function to check and install required packages
function install_packages() {
  local required_packages=("curl" "docker.io" "docker-compose")
  local not_installed=()
  for package in "${required_packages[@]}"; do
    if ! dpkg -s "$package" &> /dev/null; then
      not_installed+=("$package")
    fi
  done

  if [[ ${#not_installed[@]} -gt 0 ]]; then
    echo "Installing missing packages: ${not_installed[*]}"
    sudo apt-get update && sudo apt-get install -y "${not_installed[@]}"
  else
    echo "All required packages are already installed."
  fi
}

# Function to check if Docker is installed
function install_docker() {
  if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
  else
    echo "Docker is already installed."
  fi
}

# Function to check if Docker Compose is installed
function install_docker_compose() {
  if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
  else
    echo "Docker Compose is already installed."
  fi
}

# Function to force rebuild and deploy containers
function rebuild_containers() {
  echo "Stopping and removing existing containers..."
  sudo docker-compose down --volumes --remove-orphans

  echo "Pruning unused Docker resources..."
  sudo docker system prune -a --volumes -f

  echo "Rebuilding and deploying containers..."
  sudo docker-compose up --build -d
}

# --- Main Script ---

# Step 1: Check and install required packages
install_packages

# Step 2: Install Docker if not installed
install_docker

# Step 3: Install Docker Compose if not installed
install_docker_compose

# Step 4: Rebuild and deploy containers
rebuild_containers

echo "Deployment complete!"
