@echo off
chcp 65001 >nul
echo ============================================
echo  Создание базы данных PostgreSQL
echo ============================================
echo.
echo Этот скрипт создаст базу данных 'rf37ie_knowledge_base'
echo.

for /d %%i in ("C:\Program Files\PostgreSQL\*") do (
    if exist "%%i\bin\createdb.exe" (
        echo Найден PostgreSQL: %%i
        set PGPASSWORD=postgres
        "%%i\bin\createdb" -U postgres rf37ie_knowledge_base 2>nul
        if %ERRORLEVEL% EQU 0 (
            echo База данных успешно создана!
        ) else (
            echo База данных уже существует или ошибка создания
        )
        pause
        exit /b 0
    )
)

echo PostgreSQL не найден автоматически.
echo.
echo Создайте базу вручную через pgAdmin:
echo   Имя: rf37ie_knowledge_base
echo   Владелец: postgres
pause