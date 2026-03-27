#!/usr/bin/env python3
"""
Advanced Email Extractor
Продвинутый парсер email-адресов с сайтов компаний
"""

import requests
import re
import sqlite3
import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedEmailExtractor:
    """
    Продвинутый извлекатель email-адресов
    """
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        })
        
        # Паттерны для поиска email
        self.email_patterns = [
            re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            # Защита от спам-ботов
            re.compile(r'[a-zA-Z0-9._%+-]+\s*\[at\]\s*[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'),
            re.compile(r'[a-zA-Z0-9._%+-]+\s*@\s*[a-zA-Z0-9.-]+\s*\.\s*[a-zA-Z]{2,}'),
        ]
        
        # Список путей для проверки
        self.contact_paths = [
            '/contacts', '/contact', '/kontakty', '/kontakt',
            '/about', '/about-us', '/o-nas',
            '/feedback', '/feedback/', '/write-us',
            '/support', '/help',
            '/company', '/company/',
            '/connect', '/get-in-touch',
            '/requisites', '/rekvizity',
        ]
        
        self.visited = set()
        self.found_emails = {}
    
    def normalize_url(self, url):
        """Нормализация URL"""
        if not url:
            return None
        
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Убираем завершающий слэш
        url = url.rstrip('/')
        
        return url
    
    def is_valid_email(self, email):
        """Проверка валидности и фильтрация ложных срабатываний"""
        if not email or len(email) > 100:
            return False
        
        email = email.lower().strip()
        
        # Фильтрация
        invalid_patterns = [
            r'@example\.',
            r'@test\.',
            r'@domain\.',
            r'@email\.',
            r'\.png@',
            r'\.jpg@',
            r'\.gif@',
            r'@w3\.',
            r'@yourdomain',
            r'@company\.',
            r'^root@',
            r'^admin@localhost',
            r'^postmaster@',
            r'^webmaster@',
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, email):
                return False
        
        # Проверка на похожие на файлы
        if re.search(r'\.(jpg|jpeg|png|gif|pdf|doc|zip|rar)@', email):
            return False
        
        return True
    
    def decode_protected_email(self, text):
        """Декодирование защищённых email (например, email[at]domain.com)"""
        # Замена [at] на @
        decoded = re.sub(r'\s*\[at\]\s*', '@', text, flags=re.IGNORECASE)
        decoded = re.sub(r'\s*@\s*', '@', decoded)
        decoded = re.sub(r'\s*\.\s*', '.', decoded)
        return decoded
    
    def fetch_url(self, url, timeout=15, retries=2):
        """Загрузка URL с повторами"""
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=timeout, allow_redirects=True)
                response.raise_for_status()
                
                # Определяем кодировку
                if response.encoding == 'ISO-8859-1':
                    response.encoding = 'utf-8'
                
                return response.text
                
            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on {url}, attempt {attempt + 1}")
                time.sleep(2)
            except requests.exceptions.RequestException as e:
                logger.debug(f"Request error for {url}: {e}")
                return None
        
        return None
    
    def extract_from_page(self, html, base_url):
        """Извлечение email из HTML страницы"""
        emails = set()
        
        if not html:
            return emails
        
        # 1. Прямой поиск в HTML
        for pattern in self.email_patterns:
            matches = pattern.findall(html)
            for match in matches:
                decoded = self.decode_protected_email(match)
                if self.is_valid_email(decoded):
                    emails.add(decoded.lower())
        
        # 2. Поиск в mailto: ссылках
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('mailto:'):
                email = href[7:].split('?')[0]  # Убираем параметры
                if self.is_valid_email(email):
                    emails.add(email.lower())
        
        # 3. Поиск в тексте ссылки
        for link in soup.find_all('a'):
            text = link.get_text()
            for pattern in self.email_patterns:
                matches = pattern.findall(text)
                for match in matches:
                    if self.is_valid_email(match):
                        emails.add(match.lower())
        
        return emails
    
    def find_contact_pages(self, base_url, html):
        """Поиск страниц контактов на сайте"""
        contact_urls = []
        
        if not html:
            return contact_urls
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Ищем ссылки на страницы контактов
        for link in soup.find_all('a', href=True):
            href = link['href']
            text = link.get_text().lower()
            
            # Проверяем текст ссылки
            contact_keywords = ['контакт', 'contact', 'связаться', 'написать', 'feedback']
            if any(kw in text for kw in contact_keywords):
                full_url = urljoin(base_url, href)
                contact_urls.append(full_url)
            
            # Проверяем URL
            if any(path in href.lower() for path in self.contact_paths):
                full_url = urljoin(base_url, href)
                contact_urls.append(full_url)
        
        # Добавляем стандартные пути
        for path in self.contact_paths:
            contact_urls.append(urljoin(base_url, path))
        
        # Уникальность
        return list(set(contact_urls))[:10]  # Максимум 10 страниц
    
    def parse_website(self, website):
        """Полный парсинг сайта компании"""
        base_url = self.normalize_url(website)
        if not base_url:
            return set()
        
        domain = urlparse(base_url).netloc
        if domain in self.visited:
            return self.found_emails.get(domain, set())
        
        self.visited.add(domain)
        all_emails = set()
        
        logger.info(f"Parsing: {base_url}")
        
        # 1. Главная страница
        main_html = self.fetch_url(base_url)
        if main_html:
            emails = self.extract_from_page(main_html, base_url)
            all_emails.update(emails)
            
            # Если нашли email, возможно достаточно
            if len(all_emails) >= 2:
                self.found_emails[domain] = all_emails
                return all_emails
            
            # Ищем страницы контактов
            contact_pages = self.find_contact_pages(base_url, main_html)
        else:
            contact_pages = [urljoin(base_url, path) for path in self.contact_paths]
        
        # 2. Страницы контактов
        for url in contact_pages[:5]:  # Максимум 5 страниц
            if url in self.visited:
                continue
            
            self.visited.add(url)
            html = self.fetch_url(url)
            
            if html:
                emails = self.extract_from_page(html, url)
                all_emails.update(emails)
                
                if len(all_emails) >= 3:  # Достаточно email
                    break
            
            time.sleep(0.5)
        
        self.found_emails[domain] = all_emails
        return all_emails
    
    def get_companies_to_parse(self, limit=1000):
        """Получение списка компаний для обработки"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, website 
            FROM companies 
            WHERE website IS NOT NULL 
            AND website != ''
            AND (email IS NULL OR email = '')
            AND parsed = 0
            ORDER BY RANDOM()
            LIMIT ?
        ''', (limit,))
        
        companies = cursor.fetchall()
        conn.close()
        return companies
    
    def save_emails(self, company_id, emails):
        """Сохранение найденных email"""
        if not emails:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE companies SET parsed = 1 WHERE id = ?', (company_id,))
            conn.commit()
            conn.close()
            return
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Основной email
        primary = list(emails)[0]
        
        cursor.execute('''
            UPDATE companies 
            SET email = ?, parsed = 1 
            WHERE id = ?
        ''', (primary, company_id))
        
        # Все email
        for email in emails:
            cursor.execute('''
                INSERT OR IGNORE INTO emails (company_id, email)
                VALUES (?, ?)
            ''', (company_id, email))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved {len(emails)} emails for company {company_id}")
    
    def run(self, max_workers=10, limit=1000):
        """Запуск процесса"""
        companies = self.get_companies_to_parse(limit)
        logger.info(f"Found {len(companies)} companies to process")
        
        processed = 0
        found_total = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_company = {
                executor.submit(self.parse_website, company[2]): company
                for company in companies
            }
            
            for future in as_completed(future_to_company):
                company_id, name, website = future_to_company[future]
                
                try:
                    emails = future.result()
                    self.save_emails(company_id, emails)
                    
                    processed += 1
                    found_total += len(emails)
                    
                    if processed % 10 == 0:
                        logger.info(f"Progress: {processed}/{len(companies)}, emails found: {found_total}")
                    
                except Exception as e:
                    logger.error(f"Error processing {name}: {e}")
        
        logger.info(f"Completed! Processed: {processed}, Total emails: {found_total}")


def main():
    extractor = AdvancedEmailExtractor()
    extractor.run(max_workers=15, limit=500)


if __name__ == '__main__':
    main()
