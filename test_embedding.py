# 필요한 라이브러리 설치: pip install sentence-transformers
from sentence_transformers import SentenceTransformer

# 1. 모델 로드
model_name = "intfloat/multilingual-e5-small"
model = SentenceTransformer(model_name)

# 2. 테스트 텍스트 정의 (e5 모델은 'query: ' 또는 'passage: ' 접두사가 필요합니다)
input_text = ["query: 인공지능 임베딩 모델의 차원수를 확인합니다."]

# 3. 임베딩 벡터 생성
embeddings = model.encode(input_text)

# 4. 결과 및 차원수 출력
print(f"입력 문장: {input_text[0]}")
print(f"임베딩 벡터 형태 (Shape): {embeddings.shape}")
print(f"결과 벡터의 차원수: {embeddings.shape[1]}")
