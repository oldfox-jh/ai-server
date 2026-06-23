import os
import util.common as common
from openai import OpenAI
from typing import List

class VLMProcess:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(VLMProcess, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # OpenAI client 생성
        base_url = os.environ.get("VLM_BASE_URL")
        self.client = OpenAI(
            api_key="vllm",
            base_url=base_url,
        )

    def start(self, file: str) -> str | None:
        # 프롬프트 가져옴
        with open(os.environ.get("VLM_PROMT_PATH"), "r", encoding="utf-8") as f:
            prompt = f.read()

        #base64 변환, 나중에는 직접 파일 경로 알려줌.
        base64 = common.convert_image_base64(file)

        response = self.client.chat.completions.create(
            model=os.getenv("VLM_MODEL_NAME"),
            messages=[  # type: ignore
                {
                    "role": "system",
                    "content": "You are a specialized OCR agent for scientific literature. You excel at recognizing biomedical terminology."
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text",
                         "text": f"{prompt}"},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"{base64}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=2048,
            temperature=0.2,  # OCR의 정확도를 위해 낮은 온도를 권장, 너무 낮으면..반복구문 생김
            frequency_penalty=1.0,  # 생성된 토큰이 반복되지 않도록
        )

        return response.choices[0].message.content
