#!/usr/bin/env python3
"""
Mass Data Collector
Массовый сбор данных организаций
"""

import sqlite3
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Большой список крупных городов России
CITIES = [
    'Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань',
    'Нижний Новгород', 'Челябинск', 'Самара', 'Омск', 'Ростов-на-Дону',
    'Уфа', 'Красноярск', 'Воронеж', 'Пермь', 'Волгоград',
    'Краснодар', 'Саратов', 'Тюмень', 'Тольятти', 'Ижевск',
    'Барнаул', 'Ульяновск', 'Иркутск', 'Хабаровск', 'Ярославль',
    'Владивосток', 'Махачкала', 'Томск', 'Оренбург', 'Кемерово',
    'Новокузнецк', 'Рязань', 'Набережные Челны', 'Астрахань', 'Пенза',
    'Липецк', 'Киров', 'Чебоксары', 'Тула', 'Калининград'
]

# Бизнес-категории с высоким наличием сайтов
CATEGORIES = [
    'ресторан', 'кафе', 'бар', 'столовая', 'кафетерий',
    'отель', 'гостиница', 'хостел', 'мини-отель',
    'магазин', 'супермаркет', 'торговый центр', 'бутик',
    'салон красоты', 'парикмахерская', 'SPA', 'фитнес-клуб',
    'автосервис', 'автомойка', 'шиномонтаж', 'СТО',
    'медицинский центр', 'клиника', 'стоматология', 'аптека',
    'юридические услуги', 'бухгалтерские услуги', 'аудит',
    'IT компания', 'веб-студия', 'digital-агентство',
    'строительная компания', 'риелтор', 'агентство недвижимости',
    'туристическое агентство', 'туроператор',
    'образовательный центр', 'курсы', 'тренинг',
    ' Event-агентство', 'организация праздников', 'банкетный зал',
    'логистика', 'транспортная компания', 'грузоперевозки',
    'производство', 'фабрика', 'завод',
    'оптовая компания', 'дистрибьютор', 'импортер',
    'кадровое агентство', 'рекрутинг', 'аутстаффинг',
    'маркетинговое агентство', 'PR-агентство', 'рекламное агентство',
    'фотостудия', 'видеопродакшн', ' Event-фотограф',
    'кейтеринг', 'доставка еды', 'ресторан доставки',
    'автодилер', 'автосалон', 'автолизинг',
    'страховая компания', 'страховой брокер',
    'инвестиционная компания', 'финансовый консультант',
    'архитектурное бюро', 'дизайн-студия', 'проектирование',
    'клининговая компания', 'уборка', 'химчистка',
    'охранное агентство', 'системы безопасности', 'видеонаблюдение',
    'курьерская служба', 'почта', 'доставка',
    'цветочный магазин', 'флористика', 'оформление',
    'зоомагазин', 'ветклиника', 'зоосалон',
    'мебельный салон', 'мебель на заказ', 'кухни',
    'сантехника', 'отопление', 'вентиляция',
    'электрика', 'электромонтаж', 'слаботочка',
    'окна', 'двери', 'натяжные потолки',
    'ремонт квартир', 'отделка', 'строительство',
    'недвижимость', 'застройщик', 'жилой комплекс'
]


class MassCollector:
    def __init__(self, db_path="companies.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.stats = {
            'collected': 0,
            'with_website': 0,
            'with_email': 0,
            'errors': 0
        }
    
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
        
        # Индексы для быстрого поиска
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_companies_website ON companies(website)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_companies_email ON companies(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_companies_parsed ON companies(parsed)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_companies_city ON companies(city)')
        
        conn.commit()
        conn.close()
    
    def generate_companies_batch(self, city, category, count=100):
        """Генерация реалистичных компаний"""
        import random
        
        companies = []
        streets = [
            'Ленина', 'Гагарина', 'Мира', 'Пушкина', 'Кирова',
            'Советская', 'Коммунистическая', 'Партизанская', 'Красная',
            'Центральная', 'Молодёжная', 'Школьная', 'Садовая',
            'Лесная', 'Набережная', 'Привокзальная', 'Заводская',
            'Промышленная', 'Торговая', 'Рабочая', 'Колхозная'
        ]
        
        prefixes = ['ООО', 'ИП', 'АО', 'ПАО', 'ЗАО', '']
        suffixes = ['', 'Центр', 'Плюс', 'Премиум', 'Профи', 'Сервис', 'Групп', '']
        
        for i in range(count):
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            
            name = f"{prefix} {category.title()} \"{city.split()[0]} {suffix}\"".strip()
            
            street = random.choice(streets)
            house = random.randint(1, 150)
            
            # 70% компаний имеют сайт
            has_website = random.random() > 0.3
            website = f"https://{category.replace(' ', '')}{random.randint(100,999)}-{city[:3].lower()}.ru" if has_website else ''
            
            # 40% имеют email
            has_email = random.random() > 0.6
            email = f"info@{category.replace(' ', '')}{random.randint(10,99)}.ru" if has_email else ''
            
            company = {
                'name': name,
                'address': f"{city}, ул. {street}, д. {house}",
                'city': city,
                'phone': f"+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}",
                'website': website,
                'email': email,
                'source': 'generated',
                'category': category
            }
            companies.append(company)
        
        return companies
    
    def save_companies(self, companies):
        """Потокобезопасное сохранение"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            for company in companies:
                try:
                    cursor.execute('''
                        INSERT OR IGNORE INTO companies 
                        (name, address, city, phone, website, email, source, category)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        company['name'],
                        company.get('address', ''),
                        company.get('city', ''),
                        company.get('phone', ''),
                        company.get('website', ''),
                        company.get('email', ''),
                        company.get('source', 'generated'),
                        company.get('category', '')
                    ))
                    
                    self.stats['collected'] += 1
                    if company.get('website'):
                        self.stats['with_website'] += 1
                    if company.get('email'):
                        self.stats['with_email'] += 1
                        
                except Exception as e:
                    self.stats['errors'] += 1
            
            conn.commit()
            conn.close()
    
    def generate_mass_data(self, target_count=10000):
        """Генерация массива данных"""
        logger.info(f"Starting generation of {target_count} companies...")
        
        batch_size = 500
        batches_needed = target_count // batch_size
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for batch_num in range(batches_needed):
                city = CITIES[batch_num % len(CITIES)]
                category = CATEGORIES[batch_num % len(CATEGORIES)]
                
                future = executor.submit(self.generate_companies_batch, city, category, batch_size)
                futures.append(future)
            
            for i, future in enumerate(as_completed(futures)):
                companies = future.result()
                self.save_companies(companies)
                
                if i % 5 == 0:
                    logger.info(f"Progress: {self.stats['collected']} companies generated")
        
        logger.info(f"Generation complete!")
        logger.info(f"Total: {self.stats['collected']}")
        logger.info(f"With website: {self.stats['with_website']}")
        logger.info(f"With email: {self.stats['with_email']}")
    
    def extract_emails_from_websites(self, max_workers=20):
        """Извлечение email с сайтов компаний"""
        from email_extractor import AdvancedEmailExtractor
        
        logger.info("Starting email extraction from websites...")
        
        extractor = AdvancedEmailExtractor(self.db_path)
        
        # Получаем все компании с сайтами но без email
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, name, website 
            FROM companies 
            WHERE website IS NOT NULL 
            AND website != ''
            AND (email IS NULL OR email = '')
            AND parsed = 0
        ''')
        
        companies = cursor.fetchall()
        conn.close()
        
        logger.info(f"Found {len(companies)} companies to parse")
        
        # Запускаем извлечение
        extractor.run(max_workers=max_workers, limit=len(companies))
    
    def export_all(self, output_file="mass_export.csv"):
        """Экспорт всех данных"""
        import csv
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Статистика
        cursor.execute('SELECT COUNT(*) FROM companies')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != ""')
        with_email = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE website IS NOT NULL AND website != ""')
        with_website = cursor.fetchone()[0]
        
        logger.info("=" * 50)
        logger.info("FINAL STATISTICS")
        logger.info("=" * 50)
        logger.info(f"Total companies: {total}")
        logger.info(f"With website: {with_website}")
        logger.info(f"With email: {with_email}")
        logger.info(f"Email coverage: {with_email/total*100:.1f}%")
        
        # Экспорт всех с email
        cursor.execute('''
            SELECT name, address, city, phone, website, email, category, source
            FROM companies
            WHERE email IS NOT NULL AND email != ''
            ORDER BY city, category
        ''')
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Address', 'City', 'Phone', 'Website', 'Email', 'Category', 'Source'])
            writer.writerows(rows)
        
        # Экспорт всех данных
        cursor.execute('''
            SELECT name, address, city, phone, website, email, category, source
            FROM companies
            ORDER BY city, category
        ''')
        
        rows = cursor.fetchall()
        all_file = output_file.replace('.csv', '_all.csv')
        
        with open(all_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Address', 'City', 'Phone', 'Website', 'Email', 'Category', 'Source'])
            writer.writerows(rows)
        
        conn.close()
        
        logger.info(f"✓ Exported {len(rows)} companies to {all_file}")
        logger.info(f"✓ Exported companies with email to {output_file}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Mass Data Collector')
    parser.add_argument('--generate', type=int, default=10000, help='Generate N companies')
    parser.add_argument('--extract', action='store_true', help='Extract emails from websites')
    parser.add_argument('--export', help='Export to CSV file')
    parser.add_argument('--workers', type=int, default=20, help='Number of workers')
    
    args = parser.parse_args()
    
    collector = MassCollector()
    collector.init_db()
    
    if args.generate:
        collector.generate_mass_data(args.generate)
    
    if args.extract:
        collector.extract_emails_from_websites(args.workers)
    
    if args.export:
        collector.export_all(args.export)
    else:
        collector.export_all()


if __name__ == '__main__':
    main()
