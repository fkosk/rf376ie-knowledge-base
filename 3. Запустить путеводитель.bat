@echo off
chcp 65001 >nul
title Интерактивный путеводитель

echo ============================================
echo  Русская Рыбалка Installsoft Edition 3.7.6
echo  Интерактивный путеводитель
echo ============================================
echo.

cd /d "%~dp0rf37ie_knowledge_base"

echo Сервер запущен по адресу: http://127.0.0.1:8000/
echo Для остановки сервера нажмите Ctrl + C
echo.

start "" http://127.0.0.1:8000/
python manage.py runserver

pause