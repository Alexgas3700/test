#!/bin/bash
# Push script for Alexgas3700/test repository

cd /root/.openclaw/workspace/2gis_parser

# Set remote
git remote remove origin 2>/dev/null
git remote add origin https://github.com/Alexgas3700/test.git

# Rename branch
git branch -M main

echo "=========================================="
echo "  Отправка на GitHub"
echo "=========================================="
echo ""
echo "Введи имя пользователя GitHub: Alexgas3700"
echo "Введи пароль (Personal Access Token):"
echo ""

# Push
git push -u origin main
