import os
from django.db import connection
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, login_required
from config import settings


@login_required
@api_view(['GET'])
def init_db(request):
    # superuser 확인
    if not request.user.is_superuser:
        return JsonResponse({'error': '접근이 거부되었습니다. 관리자만 접근할 수 있습니다.'}, status=403)
    else:
        project_root = settings.BASE_DIR

        init_sql_path = os.path.join(project_root, 'init.sql')

        if not os.path.exists(init_sql_path):
            return JsonResponse({'error': 'init.sql 파일을 찾을 수 없습니다.'}, status=404)

        with open(init_sql_path, 'r', encoding='utf-8') as file:
            sql_statements = file.read()
            with connection.cursor() as cursor:
                cursor.execute(sql_statements)

        return JsonResponse({'message': 'Database initialized successfully'})