#!/usr/bin/env python3
import json
import os

def process():
    with open('oraciones_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    os.makedirs('app/src/main/assets', exist_ok=True)
    
    with open('app/src/main/assets/oraciones.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    
    print(f"✓ Procesados: {len(data)} artículos")

if __name__ == "__main__":
    process()
