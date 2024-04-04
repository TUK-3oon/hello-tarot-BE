# 베이스 이미지로 Ubuntu 22.04 사용
FROM ubuntu:22.04

# Ubuntu 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && \
    apt install -y python3.10 python3-pip python3.10-distutils python3.10-dev libpq-dev tzdata && \
    ln -snf /usr/share/zoneinfo/UTC /etc/localtime && echo UTC > /etc/timezone && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 설정
WORKDIR /app

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 필요한 Python 패키지 설치
COPY requirements.txt /app/
RUN python3.10 -m pip install --no-cache-dir -r requirements.txt psycopg2-binary

# 소스 코드 복사
COPY . /app/

# 8080 포트 노출 및 서버 실행
EXPOSE 8080
CMD ["python3.10", "manage.py", "runserver", "0.0.0.0:8080"]
