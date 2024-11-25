#!/usr/bin/env bash
set -eou pipefail

# Function to check if Conda is installed
check_conda_installed() {
  if command -v conda &>/dev/null; then
    echo "Conda is already installed."
    return 0
  else
    echo "Conda is not installed."
    return 1
  fi
}

# Function to create the environment and install dependencies
create_environment() {
  echo "Creating Conda environment DISCOV_env with Python 3.10.15..."
  conda create --name DISCOV_env python=3.10.15 -y

  echo "Activating the DISCOV_env environment..."
  source "$(conda info --base)/etc/profile.d/conda.sh"
  conda activate DISCOV_env

  echo "Installing dependencies in DISCOV_env..."
  conda install -c fastchan fastai fastbook -y
  conda install rasterio fiona -y

  echo "Environment DISCOV_env created and dependencies installed successfully!"
}

# Main Script Logic
if check_conda_installed; then
  # If Conda is already installed, create the environment
  create_environment
else
  # Detect OS and Architecture for Miniconda installation
  case "$OSTYPE" in
    darwin*)
      case $(uname -m) in
        arm64)  DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh; ;;
        *)      DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh; ;;
      esac ;;
    linux*)
      case $(uname -m) in
        aarch64) DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh; ;;
        *)       DOWNLOAD=https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh; ;;
      esac ;;
    *) echo "Unknown OS: $OSTYPE"; exit 1 ;;
  esac

  # Detect Shell
  case "$SHELL" in
    *bin/zsh*)   SHELL_NAME=zsh; ;;
    *bin/bash*)  SHELL_NAME=bash; ;;
    *bin/fish*)  SHELL_NAME=fish; ;;
    *) echo "Unknown shell: $SHELL"; exit 1 ;;
  esac

  # Download and Install Miniconda
  echo "Downloading Miniconda installer..."
  curl -LO --no-progress-meter $DOWNLOAD
  bash Miniconda3-*.sh -b

  # Initialize Conda for the detected shell
  ~/miniconda3/bin/conda init $SHELL_NAME

  # Create the Conda environment and install dependencies
  create_environment

  # Final Message
  echo "Miniconda installed, and DISCOV_env environment created successfully with dependencies!"
  echo "Please close and reopen your terminal to activate Conda."
fi
