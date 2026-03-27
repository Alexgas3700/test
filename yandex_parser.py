#!/usr/bin/env python3
"""
Yandex Maps Parser
Сбор данных организаций из Яндекс.Карт
"""

import requests
import json
import sqlite3
import time
import re
from urllib.parse import quote

class YandexMapsParser:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Referer': 'https://yandex.ru/maps/',
        })
        self.db_path = "companies.db"
        
    def init_db(self):
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
        conn.commit()
        conn.close()
    
    def search_organizations(self, query, city="Москва", ll=None, spn=None, results=50):
        """
        Поиск организаций через API Яндекс.Карт
        """
        url = "https://search-maps.yandex.ru/v1/"
        
        params = {
            'text': f"{query} {city}",
            'type': 'biz',
            'results': results,
            'lang': 'ru_RU'
        }
        
        if self.api_key:
            params['apikey'] = self.api_key
        
        if ll:
            params['ll'] = ll
        if spn:
            params['spn'] = spn
            
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def parse_yandex_maps_web(self, query, city="Москва", pages=3):
        """
        Парсинг веб-версии Яндекс.Карт (без API ключа)
        """
        companies = []
        
        # Геокоординаты городов
        cities = {
            'москва': {'ll': '37.6176,55.7558', 'spn': '0.5,0.5'},
            'санкт-петербург': {'ll': '30.3158,59.9343', 'spn': '0.4,0.4'},
            'новосибирск': {'ll': '82.9346,55.0415', 'spn': '0.3,0.3'},
        }
        
        city_lower = city.lower()
        coords = cities.get(city_lower, cities['москва'])
        
        # API endpoint для поиска
        search_url = "https://yandex.ru/maps/api/search"
        
        for page in range(pages):
            params = {
                'text': query,
                'll': coords['ll'],
                'spn': coords['spn'],
                'results': 50,
                'skip': page * 50,
                'type': 'biz',
            }
            
            try:
                response = self.session.get(search_url, params=params, timeout=30)
                data = response.json()
                
                if 'features' in data:
                    for feature in data['features']:
                        props = feature.get('properties', {})
                        company = {
                            'name': props.get('name', ''),
                            'address': props.get('description', ''),
                            'city': city,
                            'phone': '',
                            'website': '',
                            'email': '',
                            'source': 'yandex_maps'
                        }
                        
                        # Phones
                        phones = props.get('CompanyMetaData', {}).get('Phones', [])
                        if phones:
                            company['phone'] = phones[0].get('formatted', '')
                        
                        # Website
                        url = props.get('CompanyMetaData', {}).get('url', '')
                        if url:
                            company['website'] = url
                        
                        companies.append(company)
                
                print(f"Page {page + 1}: found {len(data.get('features', []))} companies")
                time.sleep(2)
                
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
        
        return companies
    
    def save_to_db(self, companies):
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
                'yandex_maps'
            ))
        
        conn.commit()
        conn.close()
        print(f"Saved {len(companies)} companies")


def main():
    parser = YandexMapsParser()
    parser.init_db()
    
    categories = [
        'ресторан',
        'кафе', 
        'отель',
        'салон красоты',
        'автосервис',
        'строительная компания',
        'юридические услуги',
        'бухгалтерские услуги'
    ]
    
    cities = ['Москва', 'Санкт-Петербург']
    
    for city in cities:
        for category in categories:
            print(f"\nSearching: {category} in {city}")
            companies = parser.parse_yandex_maps_web(category, city, pages=2)
            parser.save_to_db(companies)
            time.sleep(3)


if __name__ == '__main__':
    main()
