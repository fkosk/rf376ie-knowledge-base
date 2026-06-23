@echo off
chcp 65001 >nul
title Интерактивный путеводитель - Установка

echo ============================================
echo  Русская Рыбалка Installsoft Edition 3.7.6
echo  Интерактивный путеводитель - Установка
echo ============================================
echo.

cd /d "%~dp0rf37ie_knowledge_base"

echo [1/4] Установка зависимостей...
pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось установить зависимости
    pause
    exit /b 1
)

echo.
echo [2/4] Создание миграций...
python manage.py makemigrations
if %ERRORLEVEL% NEQ 0 (
    echo ОШИБКА: Не удалось создать миграции
    pause
    exit /b 1
)

echo.
echo [3/4] Применение миграций...
python manage.py migrate
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ============================================
    echo  ОШИБКА: Не удалось подключиться к базе данных!
    echo.
    echo  Проверьте:
    echo  1. PostgreSQL запущен?
    echo  2. База данных 'rf37ie_knowledge_base' создана в pgAdmin?
    echo  3. Пароль пользователя postgres верный?
    echo ============================================
    pause
    exit /b 1
)

echo.
echo [4/4] Заполнение базы данных...
python manage.py populate_database
python manage.py populate_baits

echo.
echo ============================================
echo  Установка завершена!
echo  Запустите run.bat для старта сервера
echo ============================================
pause