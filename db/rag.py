import psycopg2
import db.common as common
from entity.common_response import CommonApiResponse
from util.rag.embedding_service import EmbeddingService

"""
    업로드 파일 목록 조건 없음
"""
def list_documents_files() :
    conn = None
    cursor = None
    results = None
    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * from fn.list_document();"
        cursor.execute(query)

        # 1. 컬럼명 추출
        columns = [desc[0] for desc in cursor.description]

        # 2. 데이터를 딕셔너리 리스트로 변환
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except psycopg2.Error as e:
        print(f"Error select data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return results

"""
    업로드 파일 조건 검색
"""
def list_documents_with_condition(query: str):
    conn = None
    cursor = None
    results = None
    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = " select * from fn.list_document('%s');" % query

        cursor.execute(query)

        # 1. 컬럼명 추출
        columns = [desc[0] for desc in cursor.description]

        # 2. 데이터를 딕셔너리 리스트로 변환
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except Exception as e:
        print(f"Error select data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return results

"""
    파일 정보 등록
"""
def add_document(user_uuid:str, message_uuid: str | None, file_name: str, file_type: str, save_path: str, file_size: int):
    conn = None
    cursor = None
    result = None

    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * from fn.add_document( %(user_uuid)s,%(message_uuid)s,%(file_name)s,%(file_type)s,%(save_path)s,%(file_size)s);"

        params = {
            "user_uuid": user_uuid,
            "message_uuid": message_uuid,
            "file_name": file_name,
            "file_type": file_type,
            "save_path": save_path,
            "file_size": file_size
        }

        print(query)
        cursor.execute(query, params)

        # 3. 반환된 uuid 값 가져오기
        result = cursor.fetchone()

        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return result

"""
    파일 정보 삭제
"""
def delete_document(file_uuid:str) -> CommonApiResponse:
    conn = None
    cursor = None
    response = CommonApiResponse()

    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT fn.delete_document('%s');" % file_uuid

        cursor.execute(query)
        conn.commit()
        response.success = True
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
        response.success = False
        response.message = str(e).strip()
        response.code = "ERROR"
    finally:
        cursor.close()
        conn.close()

    return response

"""
    텍스트 chunk와 임베딩된 데이터 추가
"""
def add_chunk(document_uuid:str, chunk_seq: int, content: str):
    # 임베딩 데이터 가져오기
    vector_list = EmbeddingService().embedding(content)

    conn = None
    cursor = None
    result = None

    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT fn.add_document('%s', '%s', '%s', '%s', '%s', %d);" % ()

        print(query)
        cursor.execute(query)

        # 3. 반환된 uuid 값 가져오기
        result = cursor.fetchone()
        # generated_uuid = result[0] if result else None

        conn.commit()
    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return result

