@echo off

cd /d "%~dp0"

if not exist ".venv" (
    echo Criando virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate.bat

python -m pip install --upgrade pip

pip install -r requirements.txt

mkdir Teste\Mover_aqui

python Script\main.py

pause
