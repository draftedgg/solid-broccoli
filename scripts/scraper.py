#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin, urlparse
import hashlib
import re
import unicodedata
import sys

# Forzar UTF-8 en la salida
sys.stdout.reconfigure(encoding='utf-8')

class ScraperOraciones:
    def __init__(self):
        self.base_url = "https://www.oracionesydevocionescatolicas.com"
        self.visited = set()
        self.articles = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
    def fetch_page(self, url):
        """Descarga una página forzando UTF-8"""
        try:
            response = self.session.get(url, timeout=30, allow_redirects=True)
            # Forzar UTF-8 manualmente
            response.encoding = 'utf-8'
            
            # Si aún así falla, intentar decodificar el contenido binario
            try:
                html = response.text
                # Verificar que se puede codificar a UTF-8 sin errores
                html.encode('utf-8')
            except (UnicodeEncodeError, UnicodeDecodeError):
                # Fallback: decodificar bytes directamente
                html = response.content.decode('utf-8', errors='replace')
            
            return html
        except Exception as e:
            print(f"❌ Error descargando {url}: {e}")
            return None
    
    def normalize_text(self, text):
        """Limpia y normaliza texto preservando tildes y ñ"""
        if not text:
            return ""
        # Normalizar unicode (NFC)
        text = unicodedata.normalize('NFC', text)
        # Reemplazar espacios múltiples y saltos de línea
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def get_all_links(self, url):
        """Extrae todos los links internos de una página"""
        html = self.fetch_page(url)
        if not html:
            return set()
        
        soup = BeautifulSoup(html, 'html.parser')
        links = set()
        
        for a in soup.find_all('a', href=True):
            href = a['href'].strip()
            
            # Ignorar anchors, javascript, mailto, etc.
            if href.startswith('#') or href.startswith('javascript:') or href.startswith('mailto:'):
                continue
            
            # Convertir a URL absoluta
            full_url = urljoin(url, href)
            
            # Quitar fragmentos (#)
            full_url = full_url.split('#')[0]
            
            # Solo links del mismo dominio
            parsed = urlparse(full_url)
            if self.base_url.replace('https://', '').replace('http://', '') in parsed.netloc:
                # Limpiar trailing slash para comparar mejor
                clean_url = full_url.rstrip('/')
                links.add(clean_url)
        
        return links
    
    def extract_main_content(self, soup):
        """Extrae el contenido principal de la página"""
        # Intentar encontrar el contenido principal con varios selectores
        content_parts = []
        
        # Primero intentar divs comunes de contenido
        for selector in ['div.content', 'div.post', 'div.entry', 'div.article', 
                         'div.main', 'div.text', 'td', 'div']:
            elements = soup.select(selector)
            for el in elements:
                # Ignorar elementos muy pequeños o que parezcan menús
                text = el.get_text(separator='\n', strip=True)
                if len(text) > 100:
                    # Verificar que no sea un menú (pocos links relativos al texto)
                    links_count = len(el.find_all('a'))
                    text_length = len(text)
                    if links_count / (text_length / 100 + 1) < 5:
                        content_parts.append(text)
        
        # Si no encontramos nada útil, tomar todo el body
        if not content_parts:
            body = soup.find('body')
            if body:
                content_parts = [body.get_text(separator='\n', strip=True)]
        
        # Eliminar duplicados y unir
        unique_content = []
        seen = set()
        for part in content_parts:
            normalized = self.normalize_text(part)
            if normalized and normalized not in seen and len(normalized) > 50:
                seen.add(normalized)
                unique_content.append(normalized)
        
        return '\n\n'.join(unique_content)
    
    def categorize(self, title, url):
        """Categoriza basándose en título Y URL (mucho más preciso)"""
        text = f"{title} {url}".lower()
        
        # Normalizar para buscar sin tildes
        text_normalized = unicodedata.normalize('NFD', text)
        text_normalized = ''.join(c for c in text_normalized if unicodedata.category(c) != 'Mn')
        
        # Orden importa: verificar de más específico a más general
        if any(kw in text_normalized for kw in ['rosario', 'rosarios']):
            return 'rosarios'
        if any(kw in text_normalized for kw in ['novena', 'novenas']):
            return 'novenas'
        if any(kw in text_normalized for kw in ['devocion', 'devociones', 'devoto']):
            return 'devociones'
        if any(kw in text_normalized for kw in ['mensaje', 'mensajes']):
            return 'mensajes'
        if any(kw in text_normalized for kw in ['biblioteca', 'libro', 'libros', 'capitulo']):
            return 'biblioteca'
        if any(kw in text_normalized for kw in ['oracion', 'oraciones', 'reza', 'rezar', 'plegaria']):
            return 'oraciones'
        if any(kw in text_normalized for kw in ['santo', 'santos', 'santa', 'virgen', 'jesus', 'cristo', 'dios', 'biblia']):
            return 'devociones'
        
        return 'otros'
    
    def extract_content(self, url):
        """Extrae el contenido completo de una página"""
        html = self.fetch_page(url)
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Título
        title = "Sin título"
        title_tag = soup.find('title')
        if title_tag:
            title = self.normalize_text(title_tag.get_text())
            # Quitar el nombre del sitio del título si está presente
            title = re.sub(r'\s*[-|]\s*Oraciones.*$', '', title, flags=re.IGNORECASE)
            title = title.strip()
        
        # Si no hay título válido, usar el primer h1
        if not title or title == "Sin título" or len(title) < 5:
            h1 = soup.find('h1')
            if h1:
                title = self.normalize_text(h1.get_text())
        
        # Contenido
        content = self.extract_main_content(soup)
        
        # Si el contenido es muy corto, probablemente no es una página de contenido
        if len(content) < 200:
            return None
        
        # Generar ID único basado en URL
        article_id = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        # Categorizar
        category = self.categorize(title, url)
        
        return {
            'id': article_id,
            'url': url,
            'title': title,
            'content': content,
            'category': category,
            'isFavorite': False
        }
    
    def crawl(self, start_url):
        """Recorre TODO el sitio sin límite"""
        to_visit = [start_url.rstrip('/')]
        pages_scraped = 0
        consecutive_errors = 0
        max_consecutive_errors = 50
        
        print(f"🚀 Iniciando scraping de {self.base_url}")
        print("Esto puede tardar varios minutos...\n")
        
        while to_visit and consecutive_errors < max_consecutive_errors:
            url = to_visit.pop(0)
            
            if url in self.visited:
                continue
            
            self.visited.add(url)
            
            try:
                print(f"[{pages_scraped + 1}] {url}")
                
                # Extraer contenido
                article = self.extract_content(url)
                if article:
                    self.articles.append(article)
                    pages_scraped += 1
                    consecutive_errors = 0
                else:
                    # No es una página de contenido, pero seguimos
                    pass
                
                # Obtener nuevos links
                new_links = self.get_all_links(url)
                for link in new_links:
                    if link not in self.visited:
                        to_visit.append(link)
                
                # Respetar el servidor
                time.sleep(0.5)
                
            except Exception as e:
                print(f"⚠️ Error en {url}: {e}")
                consecutive_errors += 1
                time.sleep(2)
        
        print(f"\n✅ Scraping completado!")
        return self.articles
    
    def print_stats(self):
        """Imprime estadísticas del scraping"""
        categories = {}
        for article in self.articles:
            cat = article['category']
            categories[cat] = categories.get(cat, 0) + 1
        
        print("\n📊 ESTADÍSTICAS:")
        print(f"Total de artículos: {len(self.articles)}")
        print("Por categoría:")
        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            print(f"  • {cat}: {count}")
    
    def save(self, filename='oraciones_data.json'):
        """Guarda el contenido en JSON con UTF-8 correcto"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Guardado en {filename}")

if __name__ == "__main__":
    scraper = ScraperOraciones()
    scraper.crawl(scraper.base_url)
    scraper.print_stats()
    scraper.save()
    print("\n🎉 ¡Proceso terminado!")
