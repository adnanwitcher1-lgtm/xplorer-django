@echo off
REM One-shot setup for Windows
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations agency
python manage.py migrate
python manage.py seed_data
echo.
echo Done. Start the site with:  venv\Scripts\activate ^&^& python manage.py runserver
echo Site:  http://127.0.0.1:8000/     Admin: http://127.0.0.1:8000/admin/  (admin / admin12345)
