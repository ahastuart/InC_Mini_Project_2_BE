from flask import *
import pymysql
from dbconn.DBconn import *
from werkzeug.security import check_password_hash, generate_password_hash
import re
import logging

# user.log 파일에 별도로 발생하는 log 저장
logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def user_login_service():

    print("Request data:", request.json)

    id = request.json['id']
    pw = request.json['password']
    
    logging.info(f'Login attempt for user: {id}')
    cursor = dbconn.get_db().cursor(pymysql.cursors.DictCursor)
    
    SQL = "SELECT * FROM users WHERE email = %s"
    try:
        cursor.execute(SQL, (id,))
        user = cursor.fetchone()

        # 조회 결과 하나 이상이고 비밀번호가 일치하는 경우
        if user and check_password_hash(user['password'], pw):
            # 로그인 성공 시 세션에 사용자 정보 저장
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']

            logging.info(f'Successful login for user: {id}')
            print(session)
            return jsonify({
                'success': True,
                'message': user
            }), 200
        
        # 조회 결과 없거나 비밀번호가 일치하지 않은 경우
        else:
            logging.warning(f'Failed login attempt for user: {id}')
            return jsonify({
                'success': False,
                'message' : '로그인 실패. 아이디 또는 비밀번호를 확인해주세요.'
            }), 500
        
    except Exception as e:
        logging.error(f'Error during login for user {id}: {str(e)}')
        return jsonify({
                'success': False,
                'message' : f"오류 발생: {str(e)}"
            }), 500
    
    finally:
        dbconn.get_db().close()

def user_register_service():
    id = request.json['id']
    name = request.json['name']
    pw = request.json['pw']
    cpw = request.json['pwcon']
    
    # 회원가입 시도
    logging.info(f'Registartion attempt for user: {id}, {name}')

    # 필수 입력 사항 모두 입력하지 않은 경우
    if not all([id, name, pw, cpw]):
        return jsonify({
                'success': False,
                'message' : "모든 필드를 입력해주세요."
            }), 500

    # 비밀번호와 비밀번호 확인이 같지 않은 경우
    if pw != cpw:
        return jsonify({
                'success': False,
                'message' : "비밀번호가 일치하지 않습니다."
            }), 500

    # 비밀번호 정책(최소 8자 & 대소문자,숫자,특수문자 포함) 검사
    if not is_valid_password(pw):
        return jsonify({
                'success': False,
                'message' : "비밀번호는 최소 8자 이상이며, 대소문자, 숫자, 특수문자를 포함해야 합니다."
            }), 500

    try:
        cursor = dbconn.get_db().cursor(pymysql.cursors.DictCursor)
        
        # 사용자 ID 중복 체크
        cursor.execute("SELECT * FROM users WHERE email = %s", (id,))
        existing_user = cursor.fetchone()
        if existing_user:
            return jsonify({
                'success': False,
                'message' : "이미 사용 중인 email입니다."
            }), 500

        # 비밀번호 해싱
        hashed_password = generate_password_hash(pw)
        
        # 이전 비밀번호 재사용 방지
        if existing_user and check_password_hash(existing_user['password'], pw):
            return jsonify({
                'success': False,
                'message' : "이전에 사용한 비밀번호는 사용할 수 없습니다."
            }), 500
        
        # 회원 정보 생성 SQL 쿼리 실행
        SQL = "INSERT INTO users (email, password, username) VALUES (%s, %s, %s)"
        cursor.execute(SQL, (id, hashed_password, name))

        flash("회원가입이 완료되었습니다. 로그인해주세요.")
        # 회원 가입 완료 로깅
        logging.info(f'Successful registration for user: {id}')
        return jsonify({
                'success': True,
                'message' : f'회원가입 되었습니다. user_id : {id}'
            }), 200
    except Exception as e:
        # 사용자 ID 중복 체크, 비밀번호 해싱, 이전 비밀번호 재사용 방지, 회원 정보 생성 쿼리 진행에서, 오류 발생 로깅
        logging.error(f'Error during registration for user: {id}: {str(e)}')
        return jsonify({
                'success': False,
                'message' : "오류가 발생했습니다! 다시 시도해주세요."
            }), 500
    finally:
        dbconn.get_db().close()

def is_valid_password(password):
    # 비밀번호 정책: 최소 8자 & 대소문자, 숫자, 특수문자 포함
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$!#%*?&]{8,}$"
    return re.match(pattern, password) is not None

def index():
    print(session)
    print(session.get('user_id')) 
    print(f"Session data after login: {session}")
    return jsonify({
                    'success': True,
                    'message' : {
                        'session_data':session
                    }
                }), 200

def logout():
    session.clear()  # 세션 데이터 제거
    return jsonify({
                    'success': True,
                    'message' : "로그아웃되었습니다."
                }), 200

def main():
    return jsonify({
                    'success': True,
                    'message' : "실행되었습니다."
                }), 200