import os
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


class DBInitAPIView(APIView):
    def get(self, request, format=None):
        # 프로젝트 루트 디렉토리 경로
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # init.sql 파일 경로
        init_sql_path = os.path.join(project_root, 'init.sql')

        # init.sql 파일 실행
        with open(init_sql_path, 'r') as file:
            sql_statements = file.read()
            with connection.cursor() as cursor:
                cursor.execute(sql_statements)

        return Response({'message': 'Database initialized successfully'})
