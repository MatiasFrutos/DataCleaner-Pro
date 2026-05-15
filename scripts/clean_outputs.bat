@echo off
chcp 65001 >nul
title DataCleaner Pro - Limpiar salidas

echo ============================================================
echo Limpiando archivos generados por DataCleaner Pro...
echo ============================================================
echo.

cd /d "%~dp0.."

if exist "data\output" (
    del /q "data\output\*.*" >nul 2>&1
)

if exist "data\reports" (
    del /q "data\reports\*.*" >nul 2>&1
)

if exist "logs\app.log" (
    del /q "logs\app.log" >nul 2>&1
)

type nul > data\output\.gitkeep
type nul > data\reports\.gitkeep
type nul > logs\app.log

echo Limpieza completada correctamente.
echo.
pause