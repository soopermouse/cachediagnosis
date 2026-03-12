# cachemed/ml/features.py
import numpy as np
from typing import Dict, List, Any


def extract_features(readings: List[Dict]) -> Dict[str, Any]:
    """Extract features from biometric readings"""
    if not readings:
        return {}

    # Sort by timestamp
    readings.sort(key=lambda x: x.get('timestamp', 0))

    # Extract heart rate values
    heart_rates = []
    for r in readings:
        val = r.get('value', {})
        if isinstance(val, dict):
            hr = val.get('heartRate')
            if hr:
                heart_rates.append(hr)

    features = {
        'latest_heart_rate': heart_rates[-1] if heart_rates else None,
        'avg_heart_rate': np.mean(heart_rates) if heart_rates else None,
        'max_heart_rate': max(heart_rates) if heart_rates else None,
        'min_heart_rate': min(heart_rates) if heart_rates else None,
        'reading_count': len(readings)
    }

    if len(heart_rates) > 1:
        features['heart_rate_std'] = np.std(heart_rates)
        features['heart_rate_trend'] = heart_rates[-1] - heart_rates[0]

    return features