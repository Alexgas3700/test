#!/bin/bash
# GitHub Push Instructions
# Инструкция по загрузке репозитория на GitHub

echo "=========================================="
echo "  Загрузка на GitHub"
echo "=========================================="
echo ""

# Проверка наличия git
if ! command -v git &> /dev/null; then
    echo "❌ Git не установлен. Установи: sudo apt install git"
    exit 1
fi

echo "✅ Git репозиторий готов"
echo ""
echo "Текущий статус:"
git status -sb
echo ""

echo "📋 Шаги для загрузки на GitHub:"
echo ""
echo "1. Создай новый репозиторий на GitHub:"
echo "   https://github.com/new"
echo ""
echo "2. Назови репозиторий, например: company-database-10k"
echo "   НЕ добавляй README (он уже есть)"
echo "   НЕ инициализируй .gitignore"
echo ""
echo "3. Скопируй URL репозитория:"
echo "   https://github.com/ТВОЙ_НИК/company-database-10k.git"
echo ""
echo "4. Выполни эти команды:"
echo ""
echo "   # Добавь удалённый репозиторий"
echo "   git remote add origin https://github.com/ТВОЙ_НИК/company-database-10k.git"
echo ""
echo "   # Переименуй ветку в main (опционально)"
echo "   git branch -M main"
echo ""
echo "   # Отправь на GitHub"
echo "   git push -u origin main"
echo ""
echo "⚠️  ВНИМАНИЕ: Файлы больше 100MB требуют Git LFS!"
echo "   Наши файлы ~2.4MB и ~5.6MB — всё в порядке."
echo ""
echo "5. Готово! Ссылка будет:"
echo "   https://github.com/ТВОЙ_НИК/company-database-10k"
echo ""
