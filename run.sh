#!/bin/bash
#
# Company Data Collector - Quick Start Script
# Скрипт быстрого запуска сбора данных
#

echo "=========================================="
echo "  Company Data Collector"
echo "=========================================="
echo ""

# Проверка зависимостей
check_dependencies() {
    echo "🔍 Checking dependencies..."
    
    if ! command -v python3 &> /dev/null; then
        echo "❌ Python3 not found. Please install Python 3.8+"
        exit 1
    fi
    
    if ! python3 -c "import requests" 2>/dev/null; then
        echo "⚠️  Installing required packages..."
        pip3 install --break-system-packages -r requirements.txt 2>/dev/null || pip3 install -r requirements.txt
    fi
    
    echo "✓ Dependencies OK"
    echo ""
}

# Меню выбора
show_menu() {
    echo "Select operation mode:"
    echo ""
    echo "  1) Full pipeline (collect + extract emails)"
    echo "  2) Collect from 2GIS only"
    echo "  3) Collect from Yandex Maps only"
    echo "  4) Extract emails from websites"
    echo "  5) Import from CSV file"
    echo "  6) Generate test data"
    echo "  7) Export to CSV"
    echo "  8) Show statistics"
    echo "  0) Exit"
    echo ""
}

# Полный pipeline
run_full() {
    echo "📍 Enter city (default: Москва):"
    read city
    city=${city:-Москва}
    
    echo "📂 Enter categories (space separated, default: ресторан кафе):"
    read categories
    categories=${categories:-ресторан кафе}
    
    echo "📄 Enter pages per source (default: 3):"
    read pages
    pages=${pages:-3}
    
    echo ""
    echo "🚀 Starting full pipeline..."
    python3 orchestrator.py --mode full --city "$city" --categories $categories --pages $pages
}

# Сбор из 2GIS
run_2gis() {
    echo "📍 Enter city (default: Москва):"
    read city
    city=${city:-Москва}
    
    echo "📂 Enter category (default: ресторан):"
    read category
    category=${category:-ресторан}
    
    echo "📄 Enter pages (default: 5):"
    read pages
    pages=${pages:-5}
    
    python3 orchestrator.py --mode 2gis --city "$city" --categories "$category" --pages $pages
}

# Сбор из Яндекса
run_yandex() {
    echo "📍 Enter city (default: Москва):"
    read city
    city=${city:-Москва}
    
    echo "📂 Enter category (default: ресторан):"
    read category
    category=${category:-ресторан}
    
    echo "📄 Enter pages (default: 3):"
    read pages
    pages=${pages:-3}
    
    python3 orchestrator.py --mode yandex --city "$city" --categories "$category" --pages $pages
}

# Извлечение email
run_emails() {
    echo "🔧 Enter number of workers (default: 10):"
    read workers
    workers=${workers:-10}
    
    echo "📊 Enter limit of companies (default: 1000):"
    read limit
    limit=${limit:-1000}
    
    python3 orchestrator.py --mode emails --workers $workers
}

# Импорт из CSV
run_import() {
    echo "📁 Enter CSV file path:"
    read filepath
    
    if [ -f "$filepath" ]; then
        python3 data_importer.py --import-csv "$filepath"
    else
        echo "❌ File not found: $filepath"
    fi
}

# Генерация тестовых данных
run_generate() {
    echo "🔢 Enter number of records to generate (default: 100):"
    read count
    count=${count:-100}
    
    python3 data_importer.py --generate $count
}

# Экспорт
run_export() {
    echo "📁 Enter output filename (default: export.csv):"
    read filename
    filename=${filename:-export.csv}
    
    echo "📧 Export only companies with email? (y/n, default: n):"
    read only_email
    
    if [ "$only_email" = "y" ]; then
        python3 data_importer.py --export "$filename" --only-email
    else
        python3 data_importer.py --export "$filename"
    fi
}

# Статистика
run_stats() {
    python3 data_importer.py --stats
}

# Main
main() {
    check_dependencies
    
    while true; do
        show_menu
        echo "Enter your choice:"
        read choice
        
        echo ""
        case $choice in
            1) run_full ;;
            2) run_2gis ;;
            3) run_yandex ;;
            4) run_emails ;;
            5) run_import ;;
            6) run_generate ;;
            7) run_export ;;
            8) run_stats ;;
            0) echo "👋 Goodbye!"; exit 0 ;;
            *) echo "❌ Invalid option" ;;
        esac
        
        echo ""
        echo "Press Enter to continue..."
        read
        clear
    done
}

main
