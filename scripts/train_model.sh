#!/bin/bash
# cachemed/scripts/train_model.sh

echo "========================================="
echo "Cachemed Model Training Script"
echo "========================================="

# Set environment
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Default values
DATA_PATH=${1:-"data/readings.csv"}
OUTPUT_PATH=${2:-"models/cachemed_fusion.pt"}
EPOCHS=${3:-100}
BATCH_SIZE=${4:-32}

echo "Data path: $DATA_PATH"
echo "Output path: $OUTPUT_PATH"
echo "Epochs: $EPOCHS"
echo "Batch size: $BATCH_SIZE"
echo ""

# Check if data exists
if [ ! -f "$DATA_PATH" ]; then
    echo "Warning: Data file $DATA_PATH not found."
    echo "Running simple training with dummy data instead..."
    python -m ml.train_simple
else
    echo "Starting training with real data..."
    python -m ml.train \
        --data "$DATA_PATH" \
        --output "$OUTPUT_PATH" \
        --epochs "$EPOCHS" \
        --batch-size "$BATCH_SIZE"
fi

echo ""
echo "Training complete. Check $OUTPUT_PATH for model."