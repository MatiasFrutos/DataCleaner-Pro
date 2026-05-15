@echo off
chcp 65001 >nul
title DataCleaner Pro - Desarrollo

echo ============================================================
echo DataCleaner Pro - Modo desarrollo
echo ============================================================
echo.

cd /d "%~dp0.."

if not exist ".venv\Scripts\activate.bat" (
    echo No se encontró entorno virtual.
    echo Creando entorno virtual...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

echo Instalando dependencias...
pip install -r requirements.txt

echo.
echo Iniciando aplicación...
python run.py

pause