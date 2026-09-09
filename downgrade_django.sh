#!/bin/bash

echo "Memulai proses update Django dan reset migrasi..."

echo "Mencopot instalasi Django versi lama..."
pip uninstall -y django

# 2. Downgrade/Pin Django ke versi ~=5.2
echo "Menginstal Django ~=5.2..."
pip install "django~=5.2"

# 3. Menghapus semua file migrasi kecuali __init__.py (Mengabaikan folder venv/env)
echo "Menghapus file migrasi lama..."
find . -path "*/migrations/*.py" -not -path "*/env/*" -not -path "*/venv/*" -not -path "*/.venv/*" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -not -path "*/env/*" -not -path "*/venv/*" -not -path "*/.venv/*" -delete

# 4. Membuat ulang migrasi dari awal
echo "Membuat migrasi baru (makemigrations)..."
python manage.py makemigrations

# 5. Menerapkan migrasi ke database
echo "Menjalankan migrate..."
python manage.py migrate

# 6. Memperbarui requirements.txt
echo "Membekukan dependencies ke requirements.txt..."
pip freeze > requirements.txt

echo "Selesai! Versi Django saat ini:"
python -m django --version