#!/usr/bin/env python3
"""
2GIS Data Parser + Email Extractor
Сбор данных организаций из 2GIS и парсинг email с их сайтов
"""

import requests
import json
import re
import time
import csv
import sqlite3
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.init_db()
        
        # Публичные ключи 2GIS (из открытых источников/мобильного приложения)
        self.api_keys = [
            "rudcgu3317",  # старый публичный ключ
            "ruxjgr5971",  # резервный
        ]
        self.current_key_idx = 0
        
    def init_db(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                address TEXT,
                city TEXT,
                phone TEXT,
                website TEXT,
                email TEXT,
                source TEXT,
                parsed BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                email TEXT,
                source_url TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info("Database initialized")
    
    def get_api_key(self):
        """Получение текущего API ключа"""
        return self.api_keys[self.current_key_idx % len(self.api_keys)]
    
    def fetch_2gis_data(self, city, category, page=1, page_size=50):
        """
        Получение данных из 2GIS Catalog API
        """
        url = "https://catalog.api.2gis.com/3.0/items"
        
        params = {
            "key": self.get_api_key(),
            "q": category,
            "region_id": city,
            "page": page,
            "page_size": page_size,
            "fields": "items.name,items.address,items.contact_groups,items.links"
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            
            if response.status_code == 403:
                logger.warning("API key blocked, trying next...")
                self.current_key_idx += 1
                return None
                
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            return None
    
    def extract_contacts(self, item):
        """Извлечение контактов из элемента 2GIS"""
        contacts = {
            'name': item.get('name', ''),
            'address': '',
            'phone': '',
            'website': '',
            'email': ''
        }
        
        # Адрес
        if 'address_name' in item:
            contacts['address'] = item['address_name']
        elif 'address' in item:
            contacts['address'] = item['address'].get('name', '')
        
        # Контактные группы
        contact_groups = item.get('contact_groups', [])
        for group in contact_groups:
            for contact in group.get('contacts', []):
                contact_type = contact.get('type', '')
                value = contact.get('value', '')
                
                if contact_type == 'phone':
                    contacts['phone'] = value
                elif contact_type == 'website':
                    contacts['website'] = value
                elif contact_type == 'email':
                    contacts['email'] = value
        
        # Ссылки
        links = item.get('links', {})
        if 'external' in links:
            contacts['website'] = links['external']
        
        return contacts
    
    def save_to_db(self, companies):
        """Сохранение компаний в базу данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for company in companies:
            cursor.execute('''
                INSERT OR IGNORE INTO companies 
                (name, address, city, phone, website, email, source)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                company['name'],
                company.get('address', ''),
                company.get('city', ''),
                company.get('phone', ''),
                company.get('website', ''),
                company.get('email', ''),
                '2gis'
            ))
        
        conn.commit()
        conn.close()
        logger.info(f"Saved {len(companies)} companies to database")
    
    def collect_from_2gis(self, city_name, categories, max_pages=10):
        """
        Основной метод сбора данных из 2GIS
        
        city_name: название города или ID региона
        categories: список категорий для поиска
        max_pages: максимум страниц на категорию
        """
        all_companies = []
        
        # ID городов 2GIS
        city_ids = {
            'moscow': '1',
            'saint_petersburg': '2',
            'novosibirsk': '65',
            'yekaterinburg': '126',
            'kazan': '162',
        }
        
        city_id = city_ids.get(city_name.lower(), city_name)
        
        for category in categories:
            logger.info(f"Collecting: {category} in {city_name}")
            
            for page in range(1, max_pages + 1):
                data = self.fetch_2gis_data(city_id, category, page)
                
                if not data or 'result' not in data:
                    logger.warning(f"No data for page {page}")
                    break
                
                items = data['result'].get('items', [])
                if not items:
                    break
                
                for item in items:
                    contacts = self.extract_contacts(item)
                    contacts['city'] = city_name
                    all_companies.append(contacts)
                
                logger.info(f"Page {page}: collected {len(items)} items")
                time.sleep(1)  # Задержка между запросами
                
                if len(items) < 50:
                    break
        
        self.save_to_db(all_companies)
        return len(all_companies)


class EmailExtractor:
    """Извлечение email-адресов с сайтов компаний"""
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.email_pattern = re.compile(
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            re.IGNORECASE
        )
        self.visited_urls = set()
        
    def get_companies_without_email(self):
        """Получение компаний без email но с сайтом"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, website 
            FROM companies 
            WHERE (email IS NULL OR email = '') 
            AND website IS NOT NULL 
            AND website != ''
            AND parsed = 0
            LIMIT 1000
        ''')
        
        companies = cursor.fetchall()
        conn.close()
        return companies
    
    def extract_emails_from_text(self, text):
        """Извлечение email из текста"""
        emails = set()
        matches = self.email_pattern.findall(text)
        
        for email in matches:
            email = email.lower().strip()
            # Фильтрация ложных срабатываний
            if self.is_valid_email(email):
                emails.add(email)
        
        return emails
    
    def is_valid_email(self, email):
        """Проверка валидности email"""
        invalid_patterns = [
            r'@example\.',
            r'@test\.',
            r'@domain\.',
            r'@email\.',
            r'\.png$',
            r'\.jpg$',
            r'\.gif$',
            r'^noreply@',
            r'^no-reply@',
            r'^admin@',
            r'^info@example',
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email, re.IGNORECASE):
                return False
        
        return True
    
    def fetch_page(self, url, timeout=15):
        """Загрузка страницы"""
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            response = self.session.get(url, timeout=timeout, allow_redirects=True)
            response.raise_for_status()
            response.encoding = 'utf-8'
            return response.text
            
        except Exception as e:
            logger.error(f"Failed to fetch {url}: {e}")
            return None
    
    def parse_website(self, website):
        """Парсинг сайта компании для поиска email"""
        emails = set()
        pages_to_check = ['', '/contacts', '/contact', '/about', '/kontakty']
        
        base_url = website if website.startswith(('http://', 'https://')) else f'https://{website}'
        
        for page in pages_to_check:
            url = urljoin(base_url, page)
            if url in self.visited_urls:
                continue
            
            self.visited_urls.add(url)
            html = self.fetch_page(url)
            
            if html:
                page_emails = self.extract_emails_from_text(html)
                emails.update(page_emails)
                
                if emails:
                    logger.info(f"Found {len(emails)} emails on {url}")
                    break
            
            time.sleep(0.5)
        
        return emails
    
    def save_emails(self, company_id, emails, source_url):
        """Сохранение найденных email"""
        if not emails:
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Обновляем основную запись
        primary_email = list(emails)[0]
        cursor.execute('''
            UPDATE companies 
            SET email = ?, parsed = 1 
            WHERE id = ?
        ''', (primary_email, company_id))
        
        # Сохраняем все email в отдельную таблицу
        for email in emails:
            cursor.execute('''
                INSERT INTO emails (company_id, email, source_url)
                VALUES (?, ?, ?)
            ''', (company_id, email, source_url))
        
        conn.commit()
        conn.close()
    
    def mark_parsed(self, company_id):
        """Отметить компанию как обработанную"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('UPDATE companies SET parsed = 1 WHERE id = ?', (company_id,))
        conn.commit()
        conn.close()
    
    def run(self, max_workers=5, max_companies=None):
        """Запуск процесса извлечения email"""
        companies = self.get_companies_without_email()
        
        if max_companies:
            companies = companies[:max_companies]
        
        logger.info(f"Found {len(companies)} companies to process")
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_company = {}
            
            for company_id, name, website in companies:
                future = executor.submit(self.parse_website, website)
                future_to_company[future] = (company_id, name, website)
            
            for future in as_completed(future_to_company):
                company_id, name, website = future_to_company[future]
                
                try:
                    emails = future.result()
                    if emails:
                        self.save_emails(company_id, emails, website)
                        logger.info(f"{name}: found {len(emails)} emails")
                    else:
                        self.mark_parsed(company_id)
                        
                except Exception as e:
                    logger.error(f"Error processing {name}: {e}")


class EGRULParser:
    """
    Парсер данных ЕГРЮЛ/ЕГРИП из открытых источников
    """
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        
    def fetch_egrul_data(self, inn_list):
        """
        Запрос данных из API ФНС (требует токен)
        Открытые данные: https://api-fns.ru/api/egr
        """
        results = []
        
        for inn in inn_list:
            url = f"https://api-fns.ru/api/egr?req={inn}&key=YOUR_KEY"
            try:
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    data = response.json()
                    results.append(data)
            except Exception as e:
                logger.error(f"EGRUL fetch failed for {inn}: {e}")
            
            time.sleep(0.5)
        
        return results


def export_to_csv(db_path="companies.db", output_file="companies_export.csv"):
    """Экспорт данных в CSV"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT name, address, city, phone, website, email, source, created_at
        FROM companies
        WHERE email IS NOT NULL AND email != ''
        ORDER BY created_at DESC
    ''')
    
    rows = cursor.fetchall()
    
    with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'Address', 'City', 'Phone', 'Website', 'Email', 'Source', 'Created'])
        writer.writerows(rows)
    
    conn.close()
    logger.info(f"Exported {len(rows)} companies to {output_file}")


def main():
    """Основная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='2GIS Data Collector')
    parser.add_argument('--mode', choices=['2gis', 'email', 'egrul', 'export'], 
                       default='2gis', help='Режим работы')
    parser.add_argument('--city', default='moscow', help='Город для поиска')
    parser.add_argument('--categories', nargs='+', 
                       default=['ресторан', 'кафе', 'магазин', 'салон красоты'],
                       help='Категории для поиска')
    parser.add_argument('--max-pages', type=int, default=5, help='Макс. страниц')
    parser.add_argument('--workers', type=int, default=5, help='Потоков для парсинга')
    
    args = parser.parse_args()
    
    if args.mode == '2gis':
        collector = DataCollector()
        count = collector.collect_from_2gis(
            args.city, 
            args.categories, 
            args.max_pages
        )
        logger.info(f"Total collected: {count} companies")
        
    elif args.mode == 'email':
        extractor = EmailExtractor()
        extractor.run(max_workers=args.workers)
        
    elif args.mode == 'export':
        export_to_csv()
    
    else:
        logger.info("Use --mode to select operation mode")


if __name__ == '__main__':
    main()
