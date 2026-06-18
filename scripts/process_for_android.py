#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

def process():
    print("🔄 Procesando datos para Android...")
    
    # Leer con UTF-8 explícito
    with open('oraciones_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✓ Leídos {len(data)} artículos del JSON")
    
    # Estadísticas
    categories = {}
    for article in data:
        cat = article['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print("📊 Distribución por categoría:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  • {cat}: {count}")
    
    # Crear directorio de assets
    os.makedirs('app/src/main/assets', exist_ok=True)
    
    # Guardar con UTF-8 explícito
    output_path = 'app/src/main/assets/oraciones.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
    
    file_size = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n✅ Procesados {len(data)} artículos")
    print(f"📦 Tamaño del archivo: {file_size:.2f} MB")

if __name__ == "__main__":
    process()
