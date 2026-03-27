#!/usr/bin/env python3
"""
Data Collection Orchestrator
Главный скрипт управления сбором данных
"""

import argparse
import subprocess
import sys
import sqlite3
import csv
from datetime import datetime
from pathlib import Path

class Orchestrator:
    """Оркестратор процесса сбора данных"""
    
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.scripts_dir = Path(__file__).parent
    
    def init_database(self):
        """Инициализация базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Основная таблица компаний
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
        
        # Таблица всех найденных email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_id INTEGER,
                email TEXT,
                source_url TEXT,
                FOREIGN KEY (company_id) REFERENCES companies(id)
            )
        ''')
        
        # Индексы
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON companies(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_website ON companies(website)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON companies(source)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_parsed ON companies(parsed)')
        
        conn.commit()
        conn.close()
        print("✓ Database initialized")
    
    def collect_from_2gis(self, city, categories, pages):
        """Сбор данных из 2GIS"""
        print(f"\n📍 Collecting from 2GIS: {city}")
        print(f"   Categories: {', '.join(categories)}")
        
        from collector import DataCollector
        
        collector = DataCollector(self.db_path)
        count = collector.collect_from_2gis(city, categories, pages)
        print(f"✓ Collected {count} companies from 2GIS")
        return count
    
    def collect_from_yandex(self, city, categories, pages):
        """Сбор данных из Яндекс.Карт"""
        print(f"\n📍 Collecting from Yandex Maps: {city}")
        
        from yandex_parser import YandexMapsParser
        
        parser = YandexMapsParser()
        all_companies = []
        
        for category in categories:
            print(f"   Searching: {category}")
            companies = parser.parse_yandex_maps_web(category, city, pages)
            all_companies.extend(companies)
        
        parser.save_to_db(all_companies)
        print(f"✓ Collected {len(all_companies)} companies from Yandex Maps")
        return len(all_companies)
    
    def extract_emails(self, workers=10, limit=1000):
        """Извлечение email с сайтов"""
        print(f"\n📧 Extracting emails from websites...")
        print(f"   Workers: {workers}, Limit: {limit}")
        
        from email_extractor import AdvancedEmailExtractor
        
        extractor = AdvancedEmailExtractor(self.db_path)
        extractor.run(max_workers=workers, limit=limit)
        print("✓ Email extraction completed")
    
    def export_results(self, output_file=None):
        """Экспорт результатов в CSV"""
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"companies_export_{timestamp}.csv"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Статистика
        cursor.execute('SELECT COUNT(*) FROM companies')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != ""')
        with_email = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE website IS NOT NULL AND website != ""')
        with_website = cursor.fetchone()[0]
        
        print(f"\n📊 Statistics:")
        print(f"   Total companies: {total}")
        print(f"   With website: {with_website}")
        print(f"   With email: {with_email}")
        
        # Экспорт
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
        print(f"✓ Exported {len(rows)} companies with email to {output_file}")
        
        # Дополнительный экспорт - все email
        emails_file = output_file.replace('.csv', '_all_emails.csv')
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT c.name, c.city, e.email, e.source_url
            FROM emails e
            JOIN companies c ON e.company_id = c.id
            ORDER BY c.name
        ''')
        
        rows = cursor.fetchall()
        
        with open(emails_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Company', 'City', 'Email', 'Source URL'])
            writer.writerows(rows)
        
        conn.close()
        print(f"✓ Exported {len(rows)} total email records to {emails_file}")
    
    def run_full_pipeline(self, city, categories, pages=5, workers=10):
        """Полный pipeline сбора данных"""
        print("=" * 60)
        print("🚀 Starting Full Data Collection Pipeline")
        print("=" * 60)
        
        # 1. Инициализация
        self.init_database()
        
        # 2. Сбор из 2GIS
        try:
            self.collect_from_2gis(city, categories, pages)
        except Exception as e:
            print(f"⚠ 2GIS collection error: {e}")
        
        # 3. Сбор из Яндекс.Карт
        try:
            self.collect_from_yandex(city, categories, pages)
        except Exception as e:
            print(f"⚠ Yandex Maps collection error: {e}")
        
        # 4. Извлечение email
        try:
            self.extract_emails(workers=workers, limit=2000)
        except Exception as e:
            print(f"⚠ Email extraction error: {e}")
        
        # 5. Экспорт
        self.export_results()
        
        print("\n" + "=" * 60)
        print("✅ Pipeline completed!")
        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Company Data Collection System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full pipeline for Moscow restaurants
  python orchestrator.py --mode full --city Москва --categories ресторан кафе
  
  # Only collect from 2GIS
  python orchestrator.py --mode 2gis --city Москва --pages 10
  
  # Only extract emails from existing websites
  python orchestrator.py --mode emails --workers 20
  
  # Export current data
  python orchestrator.py --mode export --output results.csv
        """
    )
    
    parser.add_argument('--mode', 
                       choices=['full', '2gis', 'yandex', 'emails', 'export', 'init'],
                       default='full',
                       help='Режим работы')
    
    parser.add_argument('--city', 
                       default='Москва',
                       help='Город для поиска')
    
    parser.add_argument('--categories', 
                       nargs='+',
                       default=['ресторан', 'кафе', 'магазин'],
                       help='Категории для поиска')
    
    parser.add_argument('--pages', 
                       type=int, 
                       default=5,
                       help='Количество страниц на источник')
    
    parser.add_argument('--workers', 
                       type=int, 
                       default=10,
                       help='Количество потоков для парсинга')
    
    parser.add_argument('--output', 
                       help='Файл для экспорта')
    
    parser.add_argument('--db', 
                       default='companies.db',
                       help='Путь к базе данных')
    
    args = parser.parse_args()
    
    orch = Orchestrator(db_path=args.db)
    
    if args.mode == 'init':
        orch.init_database()
    
    elif args.mode == 'full':
        orch.run_full_pipeline(args.city, args.categories, args.pages, args.workers)
    
    elif args.mode == '2gis':
        orch.init_database()
        orch.collect_from_2gis(args.city, args.categories, args.pages)
    
    elif args.mode == 'yandex':
        orch.init_database()
        orch.collect_from_yandex(args.city, args.categories, args.pages)
    
    elif args.mode == 'emails':
        orch.extract_emails(args.workers)
    
    elif args.mode == 'export':
        orch.export_results(args.output)


if __name__ == '__main__':
    main()
