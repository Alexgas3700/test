#!/usr/bin/env python3
"""
Realistic Company Data Generator
Генератор реалистичных данных компаний с правильными email
"""

import sqlite3
import random
import string
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

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
    'event-агентство', 'организация праздников', 'банкетный зал',
    'логистика', 'транспортная компания', 'грузоперевозки',
    'производство', 'фабрика', 'завод',
    'оптовая компания', 'дистрибьютор', 'импортер',
    'кадровое агентство', 'рекрутинг', 'аутстаффинг',
    'маркетинговое агентство', 'PR-агентство', 'рекламное агентство',
    'фотостудия', 'видеопродакшн', 'event-фотограф',
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

# Транслитерация категорий для доменов
TRANSLIT_MAP = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
    'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
    'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
    'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-'
}

def translit(text):
    """Транслитерация русского текста"""
    result = ''
    for char in text.lower():
        if char in TRANSLIT_MAP:
            result += TRANSLIT_MAP[char]
        elif char in string.ascii_lowercase + string.digits + '-':
            result += char
    return result

def generate_realistic_email(category, city, index):
    """Генерация реалистичного email на латинице"""
    
    # Префиксы email
    prefixes = ['info', 'contact', 'mail', 'office', 'admin', 'sales', 'support', 
                'hello', 'manager', 'director', 'zakaz', 'booking']
    
    # Транслитерируем категорию
    cat_translit = translit(category)
    city_translit = translit(city.split()[0])  # Первое слово города
    
    # Варианты доменов
    domain_variants = [
        f"{cat_translit}{index}.ru",
        f"{cat_translit}-{city_translit}.ru",
        f"{cat_translit}-{city_translit}{index}.ru",
        f"{city_translit}-{cat_translit}.ru",
        f"{cat_translit}-group.ru",
        f"{cat_translit}-service.ru",
        f"{cat_translit}-msk.ru" if city == 'Москва' else f"{cat_translit}-spb.ru" if city == 'Санкт-Петербург' else f"{cat_translit}-{city_translit}.ru",
    ]
    
    domain = random.choice(domain_variants)
    prefix = random.choice(prefixes)
    
    return f"{prefix}@{domain}"

def generate_company_name(category, city, legal_form=None):
    """Генерация названия компании"""
    
    legal_forms = ['ООО', 'ИП', 'АО', 'ПАО', 'ЗАО', '']
    suffixes = ['', 'Центр', 'Плюс', 'Премиум', 'Профи', 'Сервис', 'Групп', 
                'Стандарт', 'Комфорт', 'Экспресс', 'Люкс', 'ВИП']
    
    lf = legal_form or random.choice(legal_forms)
    suffix = random.choice(suffixes)
    
    city_short = city.split()[0]
    
    name_variants = [
        f"{lf} {category.title()} \"{city_short} {suffix}\"".strip(),
        f"{lf} \"{category.title()} {city_short}\"".strip(),
        f"{category.title()} \"{city_short} {suffix}\"",
        f"{lf} \"{city_short} {category.title()}\"".strip(),
    ]
    
    return random.choice(name_variants)

def generate_companies_batch(city, category, count=100):
    """Генерация пачки реалистичных компаний"""
    
    companies = []
    streets = [
        'Ленина', 'Гагарина', 'Мира', 'Пушкина', 'Кирова',
        'Советская', 'Коммунистическая', 'Партизанская', 'Красная',
        'Центральная', 'Молодёжная', 'Школьная', 'Садовая',
        'Лесная', 'Набережная', 'Привокзальная', 'Заводская',
        'Промышленная', 'Торговая', 'Рабочая', 'Колхозная',
        'Октябрьская', 'Спортивная', 'Культуры', 'Горького'
    ]
    
    for i in range(count):
        street = random.choice(streets)
        house = random.randint(1, 150)
        
        # Генерируем реалистичные данные
        name = generate_company_name(category, city)
        
        # 70% компаний имеют сайт
        has_website = random.random() > 0.3
        website = ""
        email = ""
        
        if has_website:
            # Транслитерируем для сайта
            cat_translit = translit(category)
            city_translit = translit(city.split()[0])
            website = f"https://{cat_translit}-{city_translit}{random.randint(1,999)}.ru"
            
            # 60% из тех у кого сайт имеют email
            has_email = random.random() > 0.4
            if has_email:
                email = generate_realistic_email(category, city, random.randint(1,999))
        else:
            # У компаний без сайта тоже может быть email
            has_email = random.random() > 0.8
            if has_email:
                email = generate_realistic_email(category, city, random.randint(1,999))
        
        company = {
            'name': name,
            'address': f"{city}, ул. {street}, д. {house}",
            'city': city,
            'phone': f"+7 ({random.randint(900,999)}) {random.randint(100,999)}-{random.randint(10,99)}-{random.randint(10,99)}",
            'website': website,
            'email': email,
            'source': 'generated_v2',
            'category': category
        }
        companies.append(company)
    
    return companies


class RealisticDataCollector:
    def __init__(self, db_path="companies_v2.db"):
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
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON companies(email)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_city ON companies(city)')
        conn.commit()
        conn.close()
    
    def save_companies(self, companies):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for company in companies:
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
                company.get('source', 'generated_v2'),
                company.get('category', '')
            ))
        
        conn.commit()
        conn.close()
    
    def generate_mass_data(self, target_count=10000):
        logger.info(f"Generating {target_count} realistic companies...")
        
        batch_size = 500
        batches_needed = target_count // batch_size
        
        total_collected = 0
        total_with_email = 0
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for batch_num in range(batches_needed):
                city = CITIES[batch_num % len(CITIES)]
                category = CATEGORIES[batch_num % len(CATEGORIES)]
                
                future = executor.submit(generate_companies_batch, city, category, batch_size)
                futures.append(future)
            
            for i, future in enumerate(as_completed(futures)):
                companies = future.result()
                self.save_companies(companies)
                
                total_collected += len(companies)
                total_with_email += sum(1 for c in companies if c.get('email'))
                
                if i % 5 == 0:
                    logger.info(f"Progress: {total_collected} companies, {total_with_email} with email")
        
        logger.info(f"Done! Total: {total_collected}, With email: {total_with_email}")
        return total_collected, total_with_email
    
    def export_to_csv(self, output_file="companies_realistic.csv", only_with_email=True):
        import csv
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if only_with_email:
            cursor.execute('''
                SELECT name, address, city, phone, website, email, category, source
                FROM companies
                WHERE email IS NOT NULL AND email != ''
                ORDER BY city, category
            ''')
        else:
            cursor.execute('''
                SELECT name, address, city, phone, website, email, category, source
                FROM companies
                ORDER BY city, category
            ''')
        
        rows = cursor.fetchall()
        
        with open(output_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Address', 'City', 'Phone', 'Website', 'Email', 'Category', 'Source'])
            writer.writerows(rows)
        
        conn.close()
        logger.info(f"Exported {len(rows)} companies to {output_file}")
        return len(rows)
    
    def get_statistics(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM companies')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE email IS NOT NULL AND email != ""')
        with_email = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM companies WHERE website IS NOT NULL AND website != ""')
        with_website = cursor.fetchone()[0]
        
        conn.close()
        
        return {'total': total, 'with_email': with_email, 'with_website': with_website}


def main():
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--generate', type=int, default=10000)
    parser.add_argument('--export', type=str, default='companies_realistic.csv')
    parser.add_argument('--stats', action='store_true')
    
    args = parser.parse_args()
    
    collector = RealisticDataCollector()
    
    if args.generate:
        collector.generate_mass_data(args.generate)
    
    if args.export:
        collector.export_to_csv(args.export)
    
    if args.stats:
        stats = collector.get_statistics()
        print(f"\n📊 Statistics:")
        print(f"   Total: {stats['total']}")
        print(f"   With email: {stats['with_email']}")
        print(f"   With website: {stats['with_website']}")


if __name__ == '__main__':
    main()
