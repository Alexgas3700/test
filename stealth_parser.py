#!/usr/bin/env python3
"""
Protected Site Parser with Anti-Detection
Парсер с защитой от обнаружения
"""

import requests
import random
import time
import sqlite3
from bs4 import BeautifulSoup

class StealthParser:
    """
    Парсер с ротацией User-Agent и другими техниками обхода защиты
    """
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    ]
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self._rotate_identity()
    
    def _rotate_identity(self):
        """Смена User-Agent и других идентификаторов"""
        headers = {
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        self.session.headers.update(headers)
    
    def fetch_with_retry(self, url, max_retries=3, timeout=15):
        """Загрузка с повторами и задержками"""
        for attempt in range(max_retries):
            try:
                # Случайная задержка
                time.sleep(random.uniform(1, 3))
                
                response = self.session.get(url, timeout=timeout)
                
                if response.status_code == 403:
                    print(f"Access denied (403), rotating identity...")
                    self._rotate_identity()
                    continue
                
                response.raise_for_status()
                return response
                
            except requests.exceptions.RequestException as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Экспоненциальная задержка
                else:
                    raise
        
        return None


class EmailExtractorV2:
    """Улучшенный экстрактор email"""
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.parser = StealthParser(db_path)
    
    def extract_from_website(self, url):
        """Извлечение email с сайта"""
        import re
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        emails = set()
        
        try:
            response = self.parser.fetch_with_retry(url)
            if not response:
                return emails
            
            html = response.text
            
            # Поиск mailto: ссылок
            soup = BeautifulSoup(html, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('mailto:'):
                    email = href[7:].split('?')[0]
                    if self._is_valid_email(email):
                        emails.add(email.lower())
            
            # Поиск в тексте
            pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
            matches = re.findall(pattern, html)
            for email in matches:
                if self._is_valid_email(email):
                    emails.add(email.lower())
            
        except Exception as e:
            print(f"Error extracting from {url}: {e}")
        
        return emails
    
    def _is_valid_email(self, email):
        """Проверка валидности email"""
        if not email or len(email) > 100:
            return False
        
        invalid_patterns = [
            r'@example\.', r'@test\.', r'@domain\.', r'@email\.',
            r'\.png$', r'\.jpg$', r'\.gif$',
            r'^noreply@', r'^no-reply@', r'^admin@',
        ]
        
        email = email.lower()
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False
        
        return True


def main():
    print("Stealth Parser initialized")
    print("Use this module with caution and respect robots.txt")


if __name__ == '__main__':
    main()
