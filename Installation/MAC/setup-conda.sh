#!/usr/bin/env bash
set -euo pipefail

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
  echo "Activating Conda..."
  source "$HOME/miniconda3/etc/profile.d/conda.sh"

  echo "Creating Conda environment DISCOV_env with Python 3.10.15..."
  conda create --name DISCOV_env python=3.10.15 -y

  echo "Activating the DISCOV_env environment..."
  conda activate DISCOV_env

  echo "Installing dependencies in DISCOV_env..."
  conda install -c fastchan fastai fastbook -y
  conda install rasterio fiona -y

  echo "Environment DISCOV_env created and dependencies installed successfully!"
}

# Main Script Logic
if check_conda_installed; then
  create_environment
else
  # Detect OS and Architecture for Miniconda installation
  case "$OSTYPE" in
    darwin*)
      case $(uname -m) in
        arm64)  DOWNLOAD="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh" ;;
        *)      DOWNLOAD="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh" ;;
      esac ;;
    *) echo "Unsupported OS: $OSTYPE"; exit 1 ;;
  esac

  # Detect Shell
  SHELL_NAME=$(ps -p $$ -o comm= | awk -F'/' '{print $NF}')

  # Download and Install Miniconda
  echo "Downloading Miniconda installer..."
  curl -LO --no-progress-meter "$DOWNLOAD"
  curl -LO --no-progress_meter "${DOWNLOAD}.sha256"

  echo "Verifying installer integrity..."
  shasum -a 256 -c Miniconda3-latest-MacOSX-*.sh.sha256

  echo "Installing Miniconda..."
  INSTALL_DIR="$HOME/miniconda3"
  bash Miniconda3-*.sh -b -p "$INSTALL_DIR"

  echo "Cleaning up installer files..."
  rm Miniconda3-*.sh Miniconda3-*.sh.sha256

  # Initialize Conda for the detected shell
  echo "Initializing Conda for your shell..."
  "$INSTALL_DIR/bin/conda" init "$SHELL_NAME"

  # Reload shell configuration
  echo "Reloading your shell configuration..."
  case "$SHELL_NAME" in
    bash) source ~/.bash_profile ;;
    zsh)  source ~/.zshrc ;;
    *) echo "Please restart your terminal or source your shell configuration file to activate Conda." ;;
  esac

  # Create the Conda environment and install dependencies
  create_environment

  echo "Miniconda installed, and DISCOV_env environment created successfully with dependencies!"
fi
