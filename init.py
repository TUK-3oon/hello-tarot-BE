import os
from django.db import connection
from django.http import JsonResponse
from config import settings

project_root = settings.BASE_DIR

init_sql_path = os.path.join(project_root, 'init.sql')

try:
    with open(init_sql_path, 'r', encoding='utf-8') as file:
        sql_statements = file.read()
        with connection.cursor() as cursor:
            cursor.execute(sql_statements)
        print("Database initialized successfully")
except FileNotFoundError:
    print("init.sql not found.")