from flask import Blueprint, Flask, request, jsonify
from functools import wraps
from . import database_api as database
from authenticated_users import authenticated_users

mileage_bp = Blueprint('mileage', __name__)


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

        return f(current_user, *args, **kwargs)

    return decorated


@mileage_bp.route('/coupon_list', methods=["GET"])
def coupon_list():
    try:
        coupon_lists = database.get_coupon()
        return jsonify({'coupon': coupon_lists}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


@mileage_bp.route('/coupon_use/<coupon_id>', methods=["PUT"])
def coupon_use(coupon_id):
    if request.method == 'PUT':
        try:
            price = request.json.get('price')
            coupon_lists = database.get_coupon()
            return jsonify({'coupon': coupon_lists}), 200
        except Exception as e:
            print(e)
            return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


@mileage_bp.route('/donation_list', methods=["GET"])
def donation_list():
    try:
        donation_lists = database.get_donation()
        return jsonify({'coupon': donation_lists}), 200
    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
