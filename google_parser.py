#!/usr/bin/env python3
"""
Google Maps Parser
Сбор данных организаций из Google Maps
"""

import requests
import json
import sqlite3
import time
import re

class GoogleMapsParser:
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        })
        self.db_path = "companies.db"
    
    def search_places_api(self, query, location=None, radius=50000):
        """
        Использование Google Places API (требует ключ)
        """
        if not self.api_key:
            print("API key required for Places API")
            return []
        
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        
        params = {
            'query': query,
            'key': self.api_key,
            'language': 'ru'
        }
        
        if location:
            params['location'] = location
            params['radius'] = radius
        
        companies = []
        next_page_token = None
        
        for _ in range(3):  # Максимум 3 страницы
            if next_page_token:
                params['pagetoken'] = next_page_token
            
            try:
                response = self.session.get(url, params=params, timeout=30)
                data = response.json()
                
                if data.get('status') != 'OK':
                    print(f"API Error: {data.get('status')}")
                    break
                
                for place in data.get('results', []):
                    company = {
                        'name': place.get('name', ''),
                        'address': place.get('formatted_address', ''),
                        'city': self._extract_city(place.get('formatted_address', '')),
                        'phone': '',
                        'website': '',
                        'email': '',
                        'source': 'google_maps'
                    }
                    companies.append(company)
                
                next_page_token = data.get('next_page_token')
                if not next_page_token:
                    break
                
                time.sleep(2)  # Задержка для next_page_token
                
            except Exception as e:
                print(f"Error: {e}")
                break
        
        return companies
    
    def _extract_city(self, address):
        """Извлечение города из адреса"""
        parts = address.split(',')
        if len(parts) >= 2:
            return parts[-2].strip()
        return ''
    
    def get_place_details(self, place_id):
        """Получение детальной информации о месте"""
        if not self.api_key:
            return None
        
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': 'name,formatted_address,formatted_phone_number,website,url'
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            return response.json()
        except Exception as e:
            print(f"Error getting details: {e}")
            return None
    
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
                'google_maps'
            ))
        
        conn.commit()
        conn.close()
        print(f"Saved {len(companies)} companies from Google Maps")


def main():
    # Для использования нужен Google Places API key
    api_key = None  # Замените на ваш ключ
    
    parser = GoogleMapsParser(api_key=api_key)
    
    queries = [
        'рестораны Москва',
        'отели Санкт-Петербург',
        'IT компании Москва'
    ]
    
    for query in queries:
        print(f"\nSearching: {query}")
        companies = parser.search_places_api(query)
        parser.save_to_db(companies)
        time.sleep(2)


if __name__ == '__main__':
    main()
