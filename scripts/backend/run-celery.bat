@echo off
REM Celery Worker startup script (Windows)

echo Starting Celery Worker...

set "PROJECT_ROOT=d:\AutoTestingLearingProject\EasyTest-Web"
cd /d "%PROJECT_ROOT%\backend"

set PYTHONPATH=%cd%
set CELERY_BROKER_URL=redis://localhost:6379/0
set CELERY_RESULT_BACKEND=redis://localhost:6379/0

if "%CELERY_WORKER_POOL%"=="" set CELERY_WORKER_POOL=threads
if "%CELERY_WORKER_CONCURRENCY%"=="" set CELERY_WORKER_CONCURRENCY=8

"%PROJECT_ROOT%\backend\venv\Scripts\python.exe" -m celery -A app.extensions:celery -b redis://localhost:6379/0 worker --loglevel=info --pool=%CELERY_WORKER_POOL% --concurrency=%CELERY_WORKER_CONCURRENCY%

pause
