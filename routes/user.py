from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from functools import wraps
from . import database_api as database
import datetime
from authenticated_users import authenticated_users

user_bp = Blueprint('user', __name__)
# authenticated_users = {}


# 토큰 유효성 검사 및 인증된 요청 처리
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        if token in authenticated_users:
            current_user = authenticated_users[token]
        else:

            return jsonify({'message': 'Token is invalid!'}), 401
        print(current_user)
        return f(current_user, *args, **kwargs)

    return decorated


@user_bp.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        is_id = database.id_check(email, password)
        if is_id:
            token = create_access_token(identity=email, expires_delta=datetime.timedelta(seconds=100))
            authenticated_users[token] = email
            authenticated_users[token] = email
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': '잘못된 로그인 정보'}), 401


@user_bp.route('/logout', methods=["GET"])
@token_required
def logout(current_user):
    token = request.headers.get('x-access-token')
    if token in authenticated_users:
        del authenticated_users[token]
        return jsonify({"message": "로그아웃 성공"}), 200
    else:
        return jsonify({"message": "토큰이 존재하지 않습니다."}), 404


@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json.get('email')
        name = request.json.get('name')
        password = request.json.get('password')
        address = request.json.get('address')

        if database.id_duplicate_check(email):
            return jsonify({"message": "중복된 사용자"}), 500, {'Content-Type': 'application/json'}
        else:
            database.sign_up(email, name, password, address)
            return jsonify({"message": "성공"}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


@user_bp.route('/mypage', methods=["GET"])
@token_required
def mypage(current_user):
    try:
        print(current_user)
        return database.get_user(current_user)
    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
