from flask import Blueprint, request, jsonify
from authenticated_users import authenticated_users
from functools import wraps
from . import database_api as database


mypage_bp = Blueprint('mypage', __name__)

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

# 데이터베이스에서 현재 인증된 사용자의 정보를 조회
@mypage_bp.route('/profile', methods=['GET'])
@token_required
def get_user_profile(current_user):
    if current_user:
        user_info = database.get_user(current_user)
        if user_info:
            name = user_info.get('name')
            email = user_info.get('email')
            address = user_info.get('address')
            return jsonify({'name': name, 'email': email, 'address': address})
        else:
            return jsonify({'message': 'User not found'}), 404
    else:
        return jsonify({'message': 'Invalid user data'}), 400
