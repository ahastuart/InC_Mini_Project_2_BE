#----------------Dockerfile 내용----------------
# 베이스 이미지 선택 (Python 사용)
FROM python:3.9

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Nginx 설치
# RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# ec2-user 추가
# RUN useradd -m ec2-user

# 소스 코드 복사
COPY . .

# 환경 변수 파일 복사
COPY .env .env

# Nginx 설정 복사
# COPY nginx.conf /etc/nginx/nginx.conf

# 애플리케이션 실행 포트 설정
# EXPOSE 80

# Gunicorn과 Nginx 실행
#CMD ["sh", "-c", "gunicorn --bind 127.0.0.1:5000 app:app & nginx -g 'daemon off;'"]
CMD ["gunicorn", "--workers=3", "--bind=127.0.0.1:5000", "app:app"]
