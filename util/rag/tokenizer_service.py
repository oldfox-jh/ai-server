from transformers import AutoTokenizer, BertTokenizer
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from pathlib import Path


class TokenizerService:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(TokenizerService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        # 기본값: 현재 스크립트 기준으로 상대 경로 설정
        model_path = str(Path(__file__).parent / "models" / "tokenizer")

        '''
            model_name = "bert-base-multilingual-cased"
        '''
        print(f"Loading tokenizer from {model_path}...")
        self.tokenizer  = AutoTokenizer.from_pretrained(
            model_path,
            device_map="cpu",
            local_files_only=True  # 허깅페이스 허브 체크를 건너뛰고 로컬 파일만 사용
            # model_name,
        )

        self._initialized = True
        print("Tokenizer loaded")

    # 구조적 경계를 존중하는 토큰 기반 청킹 코드
    def recursive_split_text(self, text: str) -> list[str]:

        if text is None:
            raise Exception("text cannot be Empty")

        print(os.getenv("TOKENIZER_CHUNK_SIZE"))
        text_splitter = RecursiveCharacterTextSplitter.from_huggingface_tokenizer(
            tokenizer=self.tokenizer,
            chunk_size=int(os.getenv("TOKENIZER_CHUNK_SIZE")),  # 목표 토큰 수
            chunk_overlap=int(os.getenv("TOKENIZER_CHUNK_OVERLAP")),  # 중첩할 토큰 수
            separators=["\n\n", "\n", ". ", "? ", "! ", " ", ""]  # 구조적 경계 우선순위
        )

        # 청킹 실행
        chunks = text_splitter.split_text(text)

        return chunks