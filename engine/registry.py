import json
from pathlib import Path

def load_tariffs():
    tariffs = []
    for path in Path('rates').glob('*.json'):
        with open(path) as f:
            tariffs.append(json.load(f))
    return tariffs
