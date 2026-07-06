from pathlib import Path
from sentence_transformers import SentenceTransformer

class EmbeddingService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 기본값: 현재 스크립트 기준으로 상대 경로 설정
        model_path = str(Path(__file__).parent / "models" / "embedder")

        '''
            model_name = " ㅁ"
        '''
        print(f"Loading Embedder from {model_path}...")
        try:
            self.embedder = SentenceTransformer(model_path, device='cpu')
        except Exception as e:
            print(e)

        self._initialized = True
        print("Embedder loaded")

    """
        현재 임베딩 모델 : intfloat--multilingual-e5-small 384차원
    """
    def embedding(self, text_data: str) :
        embedding = self.embedder.encode(text_data)

        return embedding