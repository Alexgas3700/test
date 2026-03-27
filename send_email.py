#!/usr/bin/env python3
"""
Email Sender Script
Отправка CSV файла на указанный email
"""

import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from pathlib import Path

def send_csv_email(
    sender_email,
    sender_password,
    recipient_email,
    csv_file_path,
    subject="Company Database Export",
    smtp_server="smtp.gmail.com",
    smtp_port=587
):
    """
    Отправка CSV файла по email
    
    Параметры:
        sender_email: Ваш email
        sender_password: Пароль или app-specific password
        recipient_email: Email получателя (info@globalfinance45.ru)
        csv_file_path: Путь к CSV файлу
        subject: Тема письма
    """
    
    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    
    # Текст письма
    body = f"""
    Привет!
    
    Во вложении база данных компаний с email.
    
    Статистика:
    - Всего компаний в файле: 10,711
    - Формат: CSV
    - Размер: {os.path.getsize(csv_file_path) / 1024 / 1024:.1f} MB
    
    Структура:
    - Name: Название компании
    - Address: Адрес
    - City: Город
    - Phone: Телефон
    - Website: Сайт
    - Email: Email адрес
    - Category: Категория бизнеса
    - Source: Источник данных
    
    ---
    Сгенерировано автоматически.
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    # Прикрепляем файл
    filename = os.path.basename(csv_file_path)
    
    with open(csv_file_path, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= {filename}'
    )
    msg.attach(part)
    
    # Отправляем
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"✅ Email успешно отправлен на {recipient_email}")
        print(f"📎 Файл: {filename}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return False


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Send CSV via Email')
    parser.add_argument('--from-email', required=True, help='Ваш email')
    parser.add_argument('--password', required=True, help='Пароль от email')
    parser.add_argument('--to-email', default='info@globalfinance45.ru', help='Email получателя')
    parser.add_argument('--file', default='final_export.csv', help='Путь к CSV файлу')
    parser.add_argument('--smtp', default='smtp.gmail.com', help='SMTP сервер')
    parser.add_argument('--port', type=int, default=587, help='SMTP порт')
    
    args = parser.parse_args()
    
    # Проверяем файл
    if not os.path.exists(args.file):
        print(f"❌ Файл не найден: {args.file}")
        return
    
    # Отправляем
    send_csv_email(
        sender_email=args.from_email,
        sender_password=args.password,
        recipient_email=args.to_email,
        csv_file_path=args.file,
        smtp_server=args.smtp,
        smtp_port=args.port
    )


if __name__ == '__main__':
    # Пример использования:
    # python3 send_email.py --from-email your@gmail.com --password your_app_password --to-email info@globalfinance45.ru
    main()
