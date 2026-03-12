# cachemed/ml/model.py
import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List


class CachemedFusionModel(nn.Module):
    """Multi-modal fusion model for health prediction"""

    def __init__(self, config: Dict = None):
        super().__init__()

        if config is None:
            config = {
                'biometric_dim': 10,
                'temporal_dim': 5,
                'hidden_dim': 256
            }

        self.config = config

        # Biometric encoder
        self.biometric_encoder = nn.Sequential(
            nn.Linear(config['biometric_dim'], 128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 256)
        )

        # Temporal encoder
        self.temporal_lstm = nn.LSTM(
            input_size=config['temporal_dim'],
            hidden_size=128,
            num_layers=2,
            batch_first=True,
            bidirectional=True
        )

        # Fusion
        self.fusion = nn.Linear(256 + 256, 256)

        # Output heads
        self.cardiac_head = nn.Linear(256, 1)
        self.respiratory_head = nn.Linear(256, 1)
        self.general_head = nn.Linear(256, 1)

    def forward(self, biometrics, temporal):
        # Encode biometrics
        bio_features = self.biometric_encoder(biometrics)

        # Encode temporal
        temporal_out, _ = self.temporal_lstm(temporal)
        temporal_features = temporal_out.mean(dim=1)

        # Fuse
        combined = torch.cat([bio_features, temporal_features], dim=1)
        fused = self.fusion(combined)

        # Predictions
        cardiac = torch.sigmoid(self.cardiac_head(fused))
        respiratory = torch.sigmoid(self.respiratory_head(fused))
        general = torch.sigmoid(self.general_head(fused))

        return {
            'cardiac_risk': cardiac,
            'respiratory_risk': respiratory,
            'general_decline': general
        }

    def predict(self, readings: List[Dict]) -> Dict:
        """Simple prediction from readings"""
        if not readings:
            return {'risk': 'unknown', 'score': 0}

        # Simple rule-based prediction for demo
        latest = readings[0]
        heart_rate = latest.get('value', {}).get('heartRate', 70)

        if heart_rate > 100:
            risk = 'high'
            score = 0.8
        elif heart_rate > 80:
            risk = 'medium'
            score = 0.5
        else:
            risk = 'low'
            score = 0.2

        return {
            'risk_level': risk,
            'risk_score': score,
            'cardiac': score,
            'respiratory': score * 0.8,
            'general': score * 0.6
        }