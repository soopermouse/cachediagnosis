# cachemed/ml/train.py
# !/usr/bin/env python
"""
Training script for Cachemed ML model.
Run: python -m ml.train --data data/readings.csv --output models/cachemed_fusion.pt
"""
import argparse
import os
import sys
import json
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.model import CachemedFusionModel


class BiometricDataset(Dataset):
    """Dataset for biometric readings"""

    def __init__(self, data_path, seq_len=24):
        """
        Args:
            data_path: Path to CSV file with readings
            seq_len: Length of sequence for temporal features
        """
        self.seq_len = seq_len
        self.data = pd.read_csv(data_path)

        # Group by patient
        self.patients = self.data.groupby('patientId')
        self.samples = []

        for patient_id, group in self.patients:
            group = group.sort_values('timestamp')
            readings = group.to_dict('records')

            # Create sliding windows
            for i in range(len(readings) - seq_len):
                self.samples.append({
                    'patient_id': patient_id,
                    'sequence': readings[i:i + seq_len],
                    'target': readings[i + seq_len].get('risk_score', 0)
                })

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        sample = self.samples[idx]

        # Extract features from sequence
        sequence = sample['sequence']

        # Current biometrics (last in sequence)
        current = sequence[-1]
        biometrics = [
            current.get('heartRate', 70) / 100.0,
            current.get('hrv', 50) / 50.0,
            current.get('bloodOxygen', 98) / 100.0,
            current.get('temperature', 36.6) / 37.0,
            current.get('respiratoryRate', 16) / 20.0,
            current.get('systolic', 120) / 200.0,
            current.get('diastolic', 80) / 150.0,
            current.get('glucose', 5.5) / 10.0,
            current.get('activity', 0) / 1000.0,
            current.get('sleep', 7) / 12.0
        ]

        # Temporal sequence
        temporal = []
        for r in sequence:
            temporal.append([
                r.get('heartRate', 70) / 100.0,
                r.get('hrv', 50) / 50.0,
                r.get('bloodOxygen', 98) / 100.0,
                r.get('temperature', 36.6) / 37.0,
                r.get('activity', 0) / 1000.0
            ])

        # Metadata (placeholder - would need real data)
        metadata = [
                       hash(sample['patient_id']) % 100 / 100.0,  # Patient ID hash
                       0.5,  # age factor (placeholder)
                       0.5,  # gender factor (placeholder)
                       0.5,  # history factor (placeholder)
                   ] * 4  # Repeat to fill metadata_dim (16)

        return {
            'biometrics': torch.FloatTensor(biometrics[:10]),
            'temporal': torch.FloatTensor(temporal),
            'metadata': torch.FloatTensor(metadata[:16]),
            'target': torch.FloatTensor([sample['target']])
        }


def train_epoch(model, dataloader, optimizer, criterion, device):
    """Train for one epoch"""
    model.train()
    total_loss = 0

    for batch in dataloader:
        biometrics = batch['biometrics'].to(device)
        temporal = batch['temporal'].to(device)
        metadata = batch['metadata'].to(device)
        target = batch['target'].to(device)

        optimizer.zero_grad()

        outputs = model(biometrics, temporal, metadata)

        # Combined loss from all heads
        loss = criterion(outputs['cardiac_risk'], target) + \
               criterion(outputs['respiratory_risk'], target) + \
               criterion(outputs['general_decline'], target)

        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    return total_loss / len(dataloader)


def validate(model, dataloader, criterion, device):
    """Validate model"""
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for batch in dataloader:
            biometrics = batch['biometrics'].to(device)
            temporal = batch['temporal'].to(device)
            metadata = batch['metadata'].to(device)
            target = batch['target'].to(device)

            outputs = model(biometrics, temporal, metadata)

            loss = criterion(outputs['cardiac_risk'], target) + \
                   criterion(outputs['respiratory_risk'], target) + \
                   criterion(outputs['general_decline'], target)

            total_loss += loss.item()

    return total_loss / len(dataloader)


def main():
    parser = argparse.ArgumentParser(description='Train Cachemed model')
    parser.add_argument('--data', type=str, required=True, help='Path to training data CSV')
    parser.add_argument('--output', type=str, default='models/cachemed_fusion.pt', help='Output model path')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--seq-len', type=int, default=24, help='Sequence length')
    args = parser.parse_args()

    # Create output directory
    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    # Device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device: {device}")

    # Load dataset
    print(f"Loading data from {args.data}")
    dataset = BiometricDataset(args.data, seq_len=args.seq_len)

    # Split into train/val
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size]
    )

    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=args.batch_size, shuffle=False)

    print(f"Train samples: {len(train_dataset)}, Val samples: {len(val_dataset)}")

    # Model
    config = {
        'biometric_dim': 10,
        'temporal_dim': 5,
        'metadata_dim': 16,
        'hidden_dim': 256,
        'num_conditions': 3
    }
    model = CachemedFusionModel(config).to(device)

    # Loss and optimizer
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=args.lr)
    scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, patience=5)

    # Train
    best_val_loss = float('inf')

    for epoch in range(args.epochs):
        train_loss = train_epoch(model, train_loader, optimizer, criterion, device)
        val_loss = validate(model, val_loader, criterion, device)
        scheduler.step(val_loss)

        print(f"Epoch {epoch + 1}/{args.epochs} - Train loss: {train_loss:.4f}, Val loss: {val_loss:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), args.output)
            print(f"  -> Saved best model to {args.output}")

    print(f"Training complete. Best validation loss: {best_val_loss:.4f}")


if __name__ == '__main__':
    main()