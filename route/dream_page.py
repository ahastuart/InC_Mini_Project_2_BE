from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from comprehend.comprehend_utils import analyze_dream_content
from comprehend.com_db import save_dream, save_analysis_result
from music.music import get_playlist
from music.deepL import translate

# Blueprint 생성
bp = Blueprint('dream_page', __name__, url_prefix='/dream')

# 폼 페이지 라우트
@bp.route('', methods=['POST'])
def dream_form():
    print("받은 데이터:", request.form)

    # 폼 데이터 가져오기
    dream_content = request.form.get('dream_content', '')
    user_id = request.form.get('user_id', '')
    if not dream_content:
        flash("꿈 내용을 입력해주세요.")
        return redirect(url_for('dream_page.dream_form'))

    try:

        # 1. 꿈 내용 저장
        dream_id = save_dream(user_id, dream_content)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': '꿈 내용 저장 중 오류가 발생했습니다.',
            'error_detail': str(e)
        }), 500
    
    try:
        # 2. AWS Comprehend로 꿈 내용 분석
        en_dream_content = translate(dream_content)
        analysis_result = analyze_dream_content(dream_content)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '꿈 내용 분석 중 오류가 발생했습니다.',
            'error_detail': str(e)
        }), 500

    try:
        # 3. 분석 결과 저장
        # en_dream_content = translate(dream_content)
        save_analysis_result(dream_id, analysis_result)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': '분석 결과 저장 중 오류가 발생했습니다.',
            'error_detail': str(e)
        }), 500
    
    try:
        # 4. 감정 분석 차트 생성
        # chart_data = create_sentiment_chart_text(analysis_result)

        # 5. 추천 음악 로직 추가 (간단히 문자열로 설정)
        recommended_music = get_playlist(dream_id, analysis_result)

        # 결과 페이지 렌더링
        return jsonify({
            'success': True,
            "dream_content": dream_content,
            "analysis_result": analysis_result,
            "recommended_music": recommended_music
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': '서버 처리 중 오류가 발생했습니다.',
            'error_detail': str(e)
        }), 500

# 결과 페이지 라우트
@bp.route('/result', methods=['GET'])
def result_page():
    # URL 파라미터에서 데이터 가져오기
    dream_content = request.args.get('dream_content', '작성된 꿈이 없습니다.')
    return render_template('result.html', dream_content=dream_content)

# 시작 서비스 라우트
@bp.route('/start_service', methods=['GET'])
def start_service():
    # main.html 렌더링
    return render_template('main.html')

def inject_user():
    return {
        'email': session.get('email'),
    }

