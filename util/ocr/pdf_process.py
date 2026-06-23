from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption, ImageFormatOption
from docling_core.types.doc import TextItem, TableItem
from pathlib import Path

# 약 2G 정도 메모리 사용됨.
class DoclingProcess:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DoclingProcess, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        # 1. Docling 파이프라인 설정 (이미지 추출 활성화)
        pipeline_options = PdfPipelineOptions()
        pipeline_options.generate_picture_images = False
        pipeline_options.do_ocr = True
        pipeline_options.images_scale = 2.0  # 선명한 화질을 위한 스케일 조절

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options),
            }
        )

    def start(self, file_path: str) -> str | None:
        result_text = ""

        try:
            result = self.converter.convert(Path(file_path))
            doc = result.document

            # 1. 문서 전체 아이템 순회
            for element, _level in doc.iterate_items():
                # 이미지 아이템을 만났을 때
                if isinstance(element, TableItem):
                    table_markdown = element.export_to_markdown(doc=doc)
                    result_text += f"{table_markdown}\n"
                # 일반 텍스트 문단도 함께 RAG에 담을 때
                elif isinstance(element, TextItem):
                    result_text += f"{element.text.strip()}\n"
        except Exception as e:
            print(e)

        return result_text

