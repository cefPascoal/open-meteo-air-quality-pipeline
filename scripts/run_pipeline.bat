@echo off
setlocal

cd /d "%~dp0.."

if not defined OPEN_METEO_BASE_URL (
    echo ERRO: OPEN_METEO_BASE_URL nao esta definida.
    exit /b 1
)

if not exist logs mkdir logs

echo. >> logs\pipeline.log
echo [%date% %time%] Inicio do pipeline >> logs\pipeline.log

call .venv\Scripts\activate.bat

python -m src.main >> logs\pipeline.log 2>&1

if errorlevel 1 (
    echo [%date% %time%] ERRO: pipeline terminou com falha. >> logs\pipeline.log
    echo ERRO: pipeline terminou com falha.
    exit /b 1
)

echo [%date% %time%] Pipeline executado com sucesso. >> logs\pipeline.log
echo Pipeline executado com sucesso.

exit /b 0