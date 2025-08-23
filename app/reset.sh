#!/bin/bash

# نام دیتابیس و یوزر رو متناسب با settings.py تغییر بده
DB_NAME="django_app"
DB_USER="root"
DB_PASS="your_mysql_password"

echo "پاک کردن دیتابیس..."
mysql -u $DB_USER -p$DB_PASS -e "DROP DATABASE IF EXISTS $DB_NAME; CREATE DATABASE $DB_NAME CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;"

echo "پاک کردن فایل‌های مایگریشن..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc" -delete

echo "ساخت و اعمال مایگریشن‌ها..."
python manage.py makemigrations
python manage.py migrate

echo "تمام شد ✅ دیتابیس و مایگریشن‌ها از صفر ساخته شدند."
