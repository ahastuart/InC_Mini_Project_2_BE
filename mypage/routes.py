from flask import app, redirect, render_template, session, url_for
from dbconn.DBconn import dbconn
import pymysql
from . import mypage_bp


@mypage_bp.route('/mypage')
def mypage():
    # 세션에서 현재 로그인된 사용자 이메일 가져오기
    user_email = session.get('email')

    if not user_email:
        return redirect(url_for('user_page.user_login_service'))  # 로그인 페이지로 리다이렉트

    # 데이터베이스에서 사용자 정보 가져오기
    connection = dbconn.get_db()
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # DictCursor로 결과를 딕셔너리 형태로 반환

    try:
        # 사용자 정보 가져오기
        user_query = "SELECT id, email, username, created_date FROM users WHERE email = %s"
        cursor.execute(user_query, (user_email,))
        user_data = cursor.fetchone()

        if not user_data:
            return "사용자 정보를 찾을 수 없습니다.", 404

        # 모든 꿈 내용과 관련 노래 가져오기
        recommendations_query = """
        SELECT d.content, m.song_name
        FROM dreams d
        JOIN analysis_results ar ON d.id = ar.dream_id
        JOIN music_recommendations m ON d.id = m.dream_id 
        WHERE d.user_id = %s;
        """
        cursor.execute(recommendations_query, (user_data['id'],))
        results = cursor.fetchall()

        # 꿈 내용을 기준으로 데이터 그룹화
        recommendations = {}
        for row in results:
            content = row['content']
            song_name = row['song_name']
            if content not in recommendations:
                recommendations[content] = []
            if song_name:
                recommendations[content].append(song_name)

        return render_template('mypage.html', user_data=user_data, recommendations=recommendations)
    except Exception as e:
        print(f"Error fetching user data or recommendations: {e}")  # 디버깅용
        return f"오류 발생: {e}", 500
    finally:
        cursor.close()
        connection.close()
