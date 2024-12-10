from dbconn.DBconn import dbconn
import datetime

def save_dream(user_id, dream_content):
    """
    꿈 내용을 dreams 테이블에 저장하고 dream_id를 반환합니다.

    Parameters:
        user_id (int): 사용자 ID
        dream_content (str): 꿈 내용

    Returns:
        int: 저장된 dream_id
    """
    conn = dbconn.get_db()
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO dreams (user_id, content, input_date)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (user_id, dream_content, datetime.datetime.now()))
        conn.commit()

        # 저장된 dream_id 반환
        dream_id = cursor.lastrowid
        return dream_id
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"꿈 내용 저장 중 오류 발생: {e}")
    finally:
        conn.close()


def save_analysis_result(dream_id, analysis_result):
    """
    분석 결과를 analysis_results 테이블에 저장합니다.

    Parameters:
        dream_id (int): 관련된 꿈 ID
        analysis_result (dict): 감정 분석 결과
    """
    conn = dbconn.get_db()
    cursor = conn.cursor()

    try:
        sql = """
            INSERT INTO analysis_results (
                dream_id, positive, negative, neutral, mixed, top_sentiment, keyword
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            dream_id,
            analysis_result['positive'],
            analysis_result['negative'],
            analysis_result['neutral'],
            analysis_result['mixed'],
            analysis_result['sentiment'],
            analysis_result['keyword']
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"분석 결과 저장 중 오류 발생: {e}")
    finally:
        conn.close()
