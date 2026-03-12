#!/bin/bash
# cachemed/scripts/train_model.sh

echo "Starting model training..."

# Set environment
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run training script
python ml/train.py \
    --data data/training/readings.csv \
    --output models/cachemed_fusion.pt \
    --epochs 100 \
    --batch-size 32

echo "Training complete"