#!/usr/bin/env python3
"""
Alternative Data Sources + CSV Import
Альтернативные источники и импорт готовых данных
"""

import sqlite3
import csv
import json
import re
from pathlib import Path

class DataImporter:
    """Импорт данных из различных источников"""
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                address TEXT,
                city TEXT,
                phone TEXT,
                website TEXT,
                email TEXT,
                source TEXT,
                category TEXT,
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
    
    def import_from_csv(self, csv_file, source_name="csv_import"):
        """Импорт из CSV файла"""
        companies = []
        
        with open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Определяем поля автоматически
                company = {
                    'name': self._get_field(row, ['name', 'название', 'company', 'компания', 'Наименование', 'Организация']),
                    'address': self._get_field(row, ['address', 'адрес', 'Адрес', 'Address']),
                    'city': self._get_field(row, ['city', 'город', 'City', 'Город']),
                    'phone': self._get_field(row, ['phone', 'телефон', 'Phone', 'Телефон', 'тел']),
                    'website': self._get_field(row, ['website', 'site', 'сайт', 'Website', 'веб', 'url']),
                    'email': self._get_field(row, ['email', 'почта', 'Email', 'E-mail', 'e-mail', 'mail']),
                    'source': source_name
                }
                
                if company['name']:  # Только если есть название
                    companies.append(company)
        
        self._save_to_db(companies)
        print(f"✓ Imported {len(companies)} companies from {csv_file}")
        return len(companies)
    
    def _get_field(self, row, possible_names):
        """Получение значения по возможным названиям поля"""
        for name in possible_names:
            if name in row and row[name]:
                return row[name].strip()
        return ''
    
    def _save_to_db(self, companies):
        """Сохранение в базу данных"""
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
                company.get('source', 'import')
            ))
        
        conn.commit()
        conn.close()
    
    def import_from_json(self, json_file, source_name="json_import"):
        """Импорт из JSON файла"""
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        companies = []
        
        if isinstance(data, list):
            for item in data:
                company = self._parse_json_item(item)
                if company['name']:
                    companies.append(company)
        elif isinstance(data, dict):
            company = self._parse_json_item(data)
            if company['name']:
                companies.append(company)
        
        self._save_to_db(companies)
        print(f"✓ Imported {len(companies)} companies from {json_file}")
        return len(companies)
    
    def _parse_json_item(self, item):
        """Парсинг элемента JSON"""
        return {
            'name': item.get('name', item.get('title', item.get('company', ''))),
            'address': item.get('address', item.get('addr', '')),
            'city': item.get('city', ''),
            'phone': item.get('phone', item.get('tel', '')),
            'website': item.get('website', item.get('site', item.get('url', ''))),
            'email': item.get('email', item.get('mail', '')),
            'source': 'json_import'
        }
    
    def generate_sample_data(self, count=100):
        """Генерация тестовых данных"""
        import random
        
        cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань']
        categories = ['Ресторан', 'Кафе', 'Магазин', 'Салон красоты', 'Автосервис']
        
        companies = []
        for i in range(count):
            city = random.choice(cities)
            category = random.choice(categories)
            
            company = {
                'name': f"{category} \"Пример {i+1}\"",
                'address': f"ул. Примерная, д. {random.randint(1, 100)}",
                'city': city,
                'phone': f"+7 (9{random.randint(10, 99)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}",
                'website': f"https://example{i+1}.ru" if random.random() > 0.3 else '',
                'email': f"info@example{i+1}.ru" if random.random() > 0.5 else '',
                'source': 'generated'
            }
            companies.append(company)
        
        self._save_to_db(companies)
        print(f"✓ Generated {count} sample companies")
        return count
    
    def export_to_csv(self, output_file="export.csv", only_with_email=False):
        """Экспорт данных в CSV"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if only_with_email:
            cursor.execute('''
                SELECT name, address, city, phone, website, email, source, created_at
                FROM companies
                WHERE email IS NOT NULL AND email != ''
                ORDER BY created_at DESC
            ''')
        else:
            cursor.execute('''
                SELECT name, address, city, phone, website, email, source, created_at
                FROM companies
                ORDER BY created_at DESC
            ''')
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Address', 'City', 'Phone', 'Website', 'Email', 'Source', 'Created'])
            writer.writerows(rows)
        
        conn.close()
        print(f"✓ Exported {len(rows)} companies to {output_file}")
    
    def get_statistics(self):
        """Получение статистики"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        cursor.execute('SELECT COUNT(*) FROM companies')
        stats['total'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != ""')
        stats['with_email'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE website IS NOT NULL AND website != ""')
        stats['with_website'] = cursor.fetchone()[0]
        
        cursor.execute('SELECT source, COUNT(*) FROM companies GROUP BY source')
        stats['by_source'] = dict(cursor.fetchall())
        
        conn.close()
        return stats


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Data Import Tool')
    parser.add_argument('--import-csv', help='Импорт из CSV файла')
    parser.add_argument('--import-json', help='Импорт из JSON файла')
    parser.add_argument('--generate', type=int, help='Генерация N тестовых записей')
    parser.add_argument('--export', help='Экспорт в CSV файл')
    parser.add_argument('--only-email', action='store_true', help='Только с email')
    parser.add_argument('--stats', action='store_true', help='Показать статистику')
    
    args = parser.parse_args()
    
    importer = DataImporter()
    
    if args.import_csv:
        importer.import_from_csv(args.import_csv)
    
    elif args.import_json:
        importer.import_from_json(args.import_json)
    
    elif args.generate:
        importer.generate_sample_data(args.generate)
    
    elif args.export:
        importer.export_to_csv(args.export, args.only_email)
    
    elif args.stats:
        stats = importer.get_statistics()
        print("\n📊 Statistics:")
        print(f"   Total companies: {stats['total']}")
        print(f"   With email: {stats['with_email']}")
        print(f"   With website: {stats['with_website']}")
        print("   By source:")
        for source, count in stats['by_source'].items():
            print(f"      {source}: {count}")


if __name__ == '__main__':
    main()
