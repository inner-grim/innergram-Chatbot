# 1. Python 베이스 이미지 사용
FROM python:3.10

# 2. 작업 디렉터리 생성 및 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 애플리케이션 코드 복사
COPY . .

# 5. chatbot 디렉터리로 이동
WORKDIR /app/chatbot

# 6. 포트 설정 (uvicorn 기본 포트 8000)
EXPOSE 8000

# 7. uvicorn 서버 실행 명령어
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]