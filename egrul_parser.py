#!/usr/bin/env python3
"""
ЕГРЮЛ / ЕГРИП Parser
Работа с открытыми данными ФНС России
"""

import requests
import sqlite3
import json
import time
import csv
from datetime import datetime

class EGRULParser:
    """
    Парсер открытых данных ЕГРЮЛ и ЕГРИП
    Источники:
    - data.nalog.ru (официальный API ФНС)
    - ФИАС
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
        })
        self.db_path = "companies.db"
        
        # API endpoints
        self.fns_api_url = "https://api-fns.ru/api/"
        self.egrul_url = "https://egrul.nalog.ru"
    
    def search_by_inn(self, inn):
        """
        Поиск организации по ИНН через API ФНС
        """
        url = f"{self.egrul_url}/"
        
        # Step 1: Get captcha token
        try:
            response = self.session.get(f"{self.egrul_url}/", timeout=30)
            
            # Step 2: Submit search
            search_data = {
                'page': '',
                'query': inn,
                'region': '',
                'PreventChromeAutocomplete': ''
            }
            
            response = self.session.post(
                f"{self.egrul_url}/", 
                data=search_data, 
                timeout=30
            )
            
            result = response.json()
            
            if 'rows' in result and len(result['rows']) > 0:
                return result['rows'][0]
            
        except Exception as e:
            print(f"Error searching INN {inn}: {e}")
        
        return None
    
    def fetch_organization_details(self, token):
        """Получение детальных данных по токену"""
        url = f"{self.egrul_url}/vyp-download/"
        
        try:
            response = self.session.post(url, data={'token': token}, timeout=30)
            return response.json()
        except Exception as e:
            print(f"Error fetching details: {e}")
            return None
    
    def parse_egrul_dump(self, csv_file):
        """
        Парсинг CSV-дампа ЕГРЮЛ
        Формат: ИНН, КПП, ОГРН, Название, Адрес, ...
        """
        companies = []
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                company = {
                    'inn': row.get('ИНН', ''),
                    'kpp': row.get('КПП', ''),
                    'ogrn': row.get('ОГРН', ''),
                    'name': row.get('Наименование', ''),
                    'full_name': row.get('НаименованиеПолное', ''),
                    'address': row.get('Адрес', ''),
                    'email': row.get('ЭлектроннаяПочта', ''),
                    'phone': row.get('Телефон', ''),
                    'source': 'egrul'
                }
                companies.append(company)
        
        return companies
    
    def save_egrul_to_db(self, companies):
        """Сохранение данных ЕГРЮЛ в БД"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Создаём отдельную таблицу для ЕГРЮЛ данных
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS egrul_companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inn TEXT UNIQUE,
                kpp TEXT,
                ogrn TEXT,
                name TEXT,
                full_name TEXT,
                address TEXT,
                email TEXT,
                phone TEXT,
                source TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        for company in companies:
            cursor.execute('''
                INSERT OR REPLACE INTO egrul_companies 
                (inn, kpp, ogrn, name, full_name, address, email, phone, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                company.get('inn', ''),
                company.get('kpp', ''),
                company.get('ogrn', ''),
                company.get('name', ''),
                company.get('full_name', ''),
                company.get('address', ''),
                company.get('email', ''),
                company.get('phone', ''),
                'egrul'
            ))
        
        conn.commit()
        conn.close()
        print(f"Saved {len(companies)} companies from EGRUL")
    
    def search_by_okved(self, okved_code, region=None):
        """
        Поиск компаний по коду ОКВЭД
        """
        # Это требует доступа к расширенному API или парсинга веб-интерфейса
        pass
    
    def export_emails(self, output_file="egrul_emails.csv"):
        """Экспорт email из данных ЕГРЮЛ"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT name, inn, email, phone, address
            FROM egrul_companies
            WHERE email IS NOT NULL AND email != ''
        ''')
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'INN', 'Email', 'Phone', 'Address'])
            writer.writerows(rows)
        
        conn.close()
        print(f"Exported {len(rows)} emails to {output_file}")


class DaDataClient:
    """
    Клиент для API DaData.ru
    Стандартизация и дополнение данных по компаниям
    """
    
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.secret_key = secret_key
        self.url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party"
        
    def get_company_by_inn(self, inn):
        """Получение данных компании по ИНН"""
        headers = {
            "Authorization": f"Token {self.api_key}",
            "X-Secret": self.secret_key,
            "Content-Type": "application/json"
        }
        
        data = {"query": inn}
        
        try:
            response = requests.post(
                self.url,
                headers=headers,
                json=data,
                timeout=30
            )
            return response.json()
        except Exception as e:
            print(f"DaData error: {e}")
            return None
    
    def extract_email_from_dadata(self, suggestion):
        """Извлечение email из ответа DaData"""
        if not suggestion or 'suggestions' not in suggestion:
            return None
        
        for item in suggestion['suggestions']:
            data = item.get('data', {})
            emails = data.get('emails', [])
            if emails:
                return emails[0]
        
        return None


def download_egrul_dump():
    """
    Информация о скачивании дампов ЕГРЮЛ
    Официальные источники:
    - data.nalog.ru/opendata/ - открытые данные ФНС
    """
    print("""
    Для получения полного дампа ЕГРЮЛ:
    
    1. Официальный источник (обновляется ежемесячно):
       https://data.nalog.ru/opendata/7707329152-registerofcompanies/
    
    2. Форматы: XML, CSV
    
    3. Структура данных включает:
       - ИНН, КПП, ОГРН
       - Наименование организации
       - Юридический адрес
       - Руководители
       - Учредители
       - ОКВЭД
       
    4. Email в открытом доступе НЕ всегда присутствует
       (зависит от того, указывал ли он при регистрации)
    """)


def main():
    parser = EGRULParser()
    
    # Пример: поиск по ИНН
    test_inns = ['7707083893', '7704357909']  # Сбер, Яндекс
    
    for inn in test_inns:
        print(f"\nSearching INN: {inn}")
        result = parser.search_by_inn(inn)
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        time.sleep(2)


if __name__ == '__main__':
    # main()
    download_egrul_dump()
