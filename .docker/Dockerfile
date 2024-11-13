# 1. Python 베이스 이미지 사용
FROM python:3.10-slim

# 2. 작업 디렉터리 생성 및 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 애플리케이션 코드 복사
COPY . .

# 5. 포트 설정 (Django 기본 포트 8000)
EXPOSE 8000

# 6. Django 서버 실행 명령어
CMD ["python", "chatbot_backend/manage.py", "runserver", "0.0.0.0:8000"]