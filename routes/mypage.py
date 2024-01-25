from flask import Blueprint, request, jsonify, Flask
from authenticated_users import authenticated_users
from functools import wraps
from . import database_api as database
from flask import Flask
app = Flask(__name__)

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
        
        is_user = database.get_user_by_token(token)
  
        if is_user:
            current_user = is_user
        else:
            return jsonify({'message': 'Token is invalid!'}), 401

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


@mypage_bp.route('/get_mileage_tracking', methods=['GET', 'POST'])
@token_required
def get_mileage_tracking(current_user):
    try:
        if request.method == 'POST':
            start_date = request.json.get('start_date')
            end_date = request.json.get('end_date')
            result = database.get_tracking(current_user, start_date, end_date)
            return jsonify({'result': result}), 200
        else:
            result = database.get_all_tracking(current_user)
            return jsonify({'result': result}), 200
    except Exception as e:
        app.logger.debug(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


@mypage_bp.route('/get_mileage_info')
@token_required
def get_mileage_info(current_user):
    try:
        mileage_count = database.get_mileage_count(current_user)
        donation_count = database.get_donation_count(current_user)
        current_mileage = database.get_user_mileage(current_user)
        coupons = database.get_user_coupon(current_user)
        print(mileage_count,donation_count, current_mileage)
        response = {
            'current_mileage': current_mileage,
            'mileage_count': mileage_count,
            'donation_count': donation_count,
            'coupons': coupons
        }
        return jsonify({'result': response}), 200
    except Exception as e:
        app.logger.debug(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
