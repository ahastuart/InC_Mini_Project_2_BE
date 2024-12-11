from flask import jsonify, request, session, redirect, url_for
from dbconn.DBconn import dbconn
import pymysql
from . import mypage_bp

@mypage_bp.route('/mypage', methods=['POST'])
def fetch_mypage_data():
    # 세션에서 현재 로그인된 사용자 이메일 가져오기
    user_email = request.json['email']

    if not user_email:
        return jsonify({'error': '로그인이 필요합니다.'}), 401

    # 데이터베이스 연결
    connection = dbconn.get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # DictCursor로 결과를 딕셔너리 형태로 반환

    try:
        # 사용자 정보 가져오기
        user_query = "SELECT id, email, username, created_date FROM users WHERE email = %s"
        cursor.execute(user_query, (user_email,))
        user_data = cursor.fetchone()

        if not user_data:
            return jsonify({'error': '사용자 정보를 찾을 수 없습니다.'}), 404

        # 꿈 내용과 추천 노래 가져오기
        recommendations_query = """
        SELECT d.content, m.song_name
        FROM dreams d
        JOIN analysis_results ar ON d.id = ar.dream_id
        JOIN music_recommendations m ON d.id = m.dream_id 
        WHERE d.user_id = %s;
        """
        cursor.execute(recommendations_query, (user_data['id'],))
        results = cursor.fetchall()

        # 꿈 내용을 기준으로 추천 노래 그룹화
        recommendations = {}
        for row in results:
            content = row['content']
            song_name = row['song_name']
            if content not in recommendations:
                recommendations[content] = []
            if song_name:
                recommendations[content].append(song_name)

        # JSON 형태로 데이터 반환
        return jsonify({
            'user_data': user_data,
            'recommendations': recommendations
        })
    except Exception as e:
        print(f"Error fetching user data or recommendations: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()
