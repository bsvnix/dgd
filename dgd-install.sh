#!/bin/bash

# --- Load environment variables ---
source ./.env

# --- Functions ---

# Function to check and install packages
function install_packages() {
  local not_installed=()
  for package in "${REQUIRED_PACKAGES[@]}"; do
    if ! dpkg -s "$package" &> /dev/null; then
      not_installed+=("$package")
    fi
  done

  if [[ ${#not_installed[@]} -gt 0 ]]; then
    echo "Installing packages: ${not_installed[*]}"
    sudo apt-get update && sudo apt-get install -y "${not_installed[@]}"
  else
    echo "All required packages are already installed."
  fi
}

# Function to check if a command exists
function command_exists() {
  command -v "$1" &> /dev/null
}

# Function to install Docker (optimized)
function install_docker() {
  if ! command_exists docker; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
  else
    echo "Docker is already installed."
  fi
}

# Function to install Docker Compose (optimized)
function install_docker_compose() {
  if ! command_exists docker-compose; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
  else
    echo "Docker Compose is already installed."
  fi
}

# Function to deploy containers (with docker-compose.yml in subfolders)
function deploy_containers() {
  echo "Deploying containers..."
  sudo docker-compose up -d
}

# --- Main Script ---

# Check and install required packages
install_packages

# Check and install Docker
install_docker

# Check and install Docker Compose
install_docker_compose

# Deploy containers
deploy_containers

echo "Deployment complete!"
