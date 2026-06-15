FROM python:3.12

# 1. 필수 환경 변수 설정 (파이썬 출력 버퍼링 해제 및 pyc 파일 생성 방지)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치 (캐시 최적화를 위해 소스코드보다 먼저 복사)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn sse-starlette crewai crewai-tools psycopg2 python-dotenv transformers torch langchain_text_splitters docling accelerate docker
# 4. 도커 빌드 시점에 Docling AI 모델 미리 다운로드 (선택사항이나 권장)
# 컨테이너가 뜬 후 첫 요청 시 모델을 다운받으면 응답이 매우 느리므로 빌드 단계에서 미리 받아둡니다.
RUN python -c "from docling.document_converter import DocumentConverter; DocumentConverter()"

# 현재 디렉토리의 모든 파일과 하위 폴더를 컨테이너의 작업 디렉토리(/app)로 복사
COPY . .