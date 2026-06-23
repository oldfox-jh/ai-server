import os
import requests
import uuid
from io import BytesIO
import base64
import yaml
from openai import OpenAI

# 파일 관리
def download_pdf(url) -> str:
    # 파일명 임의로 생성.
    save_path = f"{uuid.uuid4()}.pdf"

    # 브라우저인척 해서 서버를 속임....
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers, stream=True)

    with open(save_path, "wb") as f:
        f.write(response.content)

    print(f"PDF saved to {save_path}")

    return save_path

def delete(filepath:str) -> None:
    os.remove(filepath)


# 이미지 변환
def convert_image_base64(filepath: str) -> str:
    from pathlib import Path
    extension = Path(filepath).suffix.lower().replace(".", "")

    mime_type = "jpeg" if extension in ["jpg", "jpeg"] else "png"
    # 이미지를 base64로 인코딩
    with open(filepath, "rb") as image_file:
        import base64
        image_data = base64.standard_b64encode(image_file.read()).decode("utf-8")

    return f"data:image/{mime_type};base64,{image_data}"

# yaml 파일 관리
def convert_yaml_to_dict(filepath:str) -> dict | None:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            # safe_load를 사용해야 임의의 코드 실행 취약점을 방지합니다.
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"에러: {filepath} 파일을 찾을 수 없습니다.")
    except yaml.YAMLError as exc:
        print(f"YAML 파싱 에러 발생: {exc}")

    return None