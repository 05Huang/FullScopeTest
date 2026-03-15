@echo off
REM Celery Worker startup script (Windows)

echo Starting Celery Worker...

set "SCRIPT_DIR=%~dp0"
for %%I in ("%SCRIPT_DIR%..\..") do set "PROJECT_ROOT=%%~fI"
cd /d "%PROJECT_ROOT%\backend"

set PYTHONPATH=%cd%
set CELERY_BROKER_URL=redis://localhost:6379/0
set CELERY_RESULT_BACKEND=redis://localhost:6379/0

if "%CELERY_WORKER_POOL%"=="" set CELERY_WORKER_POOL=threads
if "%CELERY_WORKER_CONCURRENCY%"=="" set CELERY_WORKER_CONCURRENCY=8

set "PYTHON_EXE=%PROJECT_ROOT%\backend\venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" set "PYTHON_EXE=python"
"%PYTHON_EXE%" -m celery -A app.extensions:celery -b redis://localhost:6379/0 worker --loglevel=info --pool=%CELERY_WORKER_POOL% --concurrency=%CELERY_WORKER_CONCURRENCY%

pause
