# Python 3.10-slim 이미지를 사용하여 기본 환경 구축
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지를 복사하고 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드를 복사
COPY . .

# 8000 포트를 외부에 개방
EXPOSE 8000

# FastAPI 서버 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "18080"]
