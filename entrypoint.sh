#!/bin/bash

# Load Conda
source /opt/miniconda/etc/profile.d/conda.sh

# Default to "mlops" unless overridden at build time
: "${ENV_NAME:=mlops}"

# Add auto-activation to .bashrc if it's not already there
#grep -qxF 'conda activate mlops' ~/.bashrc || echo 'conda activate mlops' >> ~/.bashrc
grep -qxF "conda activate $ENV_NAME" ~/.bashrc || echo "conda activate $ENV_NAME" >> ~/.bashrc

# Activate it now (for current session)
#conda activate mlops
conda activate "$ENV_NAME"

# Log in to Weights & Biases
if [ -n "$WANDB_API_KEY" ]; then
    wandb login "$WANDB_API_KEY"
fi

# Launch interactive shell or passed command
exec "$@"
