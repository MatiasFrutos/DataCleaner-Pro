@echo off
chcp 65001 >nul
title DataCleaner Pro - Build EXE

echo ============================================================
echo DataCleaner Pro - Empaquetado EXE
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

echo Instalando PyInstaller...
pip install pyinstaller

echo.
echo Generando ejecutable...
pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "DataCleanerPro" ^
    --add-data "assets;assets" ^
    --add-data "data;data" ^
    run.py

echo.
echo Build finalizado.
echo Revisar carpeta dist\
echo.
pause