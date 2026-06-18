#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import json
import time
from urllib.parse import urljoin
import hashlib

class ScraperOraciones:
    def __init__(self):
        self.base_url = "https://www.oracionesydevocionescatolicas.com"
        self.visited = set()
        self.articles = []
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
    def get_all_links(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            links = set()
            for a in soup.find_all('a', href=True):
                href = a['href']
                if href.startswith('http') or href.startswith('/'):
                    full_url = urljoin(url, href)
                    if self.base_url in full_url:
                        links.add(full_url)
            return links
        except Exception as e:
            print(f"Error: {e}")
            return set()
    
    def extract_content(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            title = soup.find('title').text if soup.find('title') else "Sin título"
            content_divs = soup.find_all(['div', 'table', 'center', 'td'])
            
            text_content = []
            for div in content_divs:
                text = div.get_text(strip=True)
                if len(text) > 50:
                    text_content.append(text)
            
            if not text_content:
                body = soup.find('body')
                if body:
                    text_content = [body.get_text(strip=True)]
            
            article_id = hashlib.md5(url.encode()).hexdigest()
            category = self.categorize(title)
            
            return {
                'id': article_id,
                'url': url,
                'title': title.strip(),
                'content': '\n\n'.join(text_content),
                'category': category,
                'isFavorite': False
            }
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def categorize(self, title):
        title_lower = title.lower()
        if 'oración' in title_lower or 'oracion' in title_lower:
            return 'oraciones'
        elif 'devoción' in title_lower or 'devocion' in title_lower:
            return 'devociones'
        elif 'mensaje' in title_lower:
            return 'mensajes'
        elif 'rosario' in title_lower:
            return 'rosarios'
        elif 'novena' in title_lower:
            return 'novenas'
        elif 'biblioteca' in title_lower or 'libro' in title_lower:
            return 'biblioteca'
        else:
            return 'otros'
    
    def crawl(self, start_url, max_pages=2000):
        to_visit = [start_url]
        pages = 0
        
        while to_visit and pages < max_pages:
            url = to_visit.pop(0)
            if url in self.visited:
                continue
            
            print(f"[{pages + 1}/{max_pages}] {url}")
            self.visited.add(url)
            
            content = self.extract_content(url)
            if content:
                self.articles.append(content)
                pages += 1
            
            new_links = self.get_all_links(url)
            to_visit.extend([l for l in new_links if l not in self.visited])
            time.sleep(1)
        
        return self.articles
    
    def save(self, filename='oraciones_data.json'):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
        print(f"✓ Guardado: {len(self.articles)} artículos")

if __name__ == "__main__":
    scraper = ScraperOraciones()
    print("🙏 Iniciando scraping...")
    scraper.crawl(scraper.base_url)
    scraper.save()
    print("✅ Completado!")
