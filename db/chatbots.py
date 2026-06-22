import psycopg2
import db.common as common
from entity.chat import ChatRequest

from entity.chatbot import ChatbotRequest
from entity.common_response import CommonApiResponse

"""
    챗봇 모델 목록 조건 없음
"""
def list_chatbot_model() :
    conn = None
    cursor = None
    results = None
    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT * from fn.list_chatbot(null, '', '', '', '');"
        cursor.execute(query)

        # 1. 컬럼명 추출
        columns = [desc[0] for desc in cursor.description]

        # 2. 데이터를 딕셔너리 리스트로 변환
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except psycopg2.Error as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return results

"""
    챗봇 모델 정보
"""
def chatbot_model(data:ChatRequest):
    conn = None
    cursor = None
    results = None
    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = " select * from fn.list_chatbot('%s'::uuid, '', '', '', '');" % data.chatbot_uuid
        params = (
            data.chatbot_uuid
        )
        cursor.execute(query, params)

        # 1. 컬럼명 추출
        columns = [desc[0] for desc in cursor.description]

        # 2. 데이터를 딕셔너리 리스트로 변환
        results = [dict(zip(columns, row)) for row in cursor.fetchall()]

    except Exception as e:
        print(f"Error inserting data: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

    return None if (results is None or len(results) == 0)  else  results[0]

"""
    챗봇 모델 정보 등록
"""
def create_chatbot_model(data:ChatbotRequest) -> CommonApiResponse:
    conn = None
    cursor = None
    response = CommonApiResponse()

    try:
        conn = common.get_chatbot_db_connection()
        cursor = conn.cursor()
        query = f"SELECT fn.add_chatbot('%s', '%s', '%s', '%s', '%s',%f, %d, '%s');" % (
            data.chatbot_name, data.description, data.model_provider, data.model_name, data.system_prompt, data.temperature, data.max_tokens, data.url
        )
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

