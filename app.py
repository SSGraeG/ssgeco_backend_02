from flask import Flask, request, jsonify
from flask_cors import CORS
import database, datetime
from os import path, remove
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
# import jwt
from functools import wraps
import os

app = Flask(__name__, static_folder='./resources/')
app.config["JWT_SECRET_KEY"] = "super-secret"
UPLOAD_FOLDER = path.join('.', 'resources/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
authenticated_users = {}

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
            return jsonify({'message' : 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def main():
    # sort = request.args.get('sort')
    # keyword = request.args.get('keyword')
    # return database.getItems(sort, keyword)
    return database.getAll()


@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        is_id = database.idCheck(email, password)
        if is_id:
            token = create_access_token(identity=email, expires_delta=datetime.timedelta(seconds=100))
            authenticated_users[token] = email
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': '잘못된 로그인 정보'}), 401


@app.route('/logout', methods=["GET"])
@token_required
def logout(current_user):
    token = request.headers.get('x-access-token')  # 클라이언트에서 전송한 토큰 가져오기
    if token in authenticated_users:  # 딕셔너리에서 토큰 확인 후 삭제
        del authenticated_users[token]

        return jsonify({"message": "로그아웃 성공"}), 200
    else:
        return jsonify({"message": "토큰이 존재하지 않습니다."}), 404


# 회원가입페이지
@app.route('/signup', methods=['POST'])
def signup():
    try:
        email = request.json.get('email')
        name = request.json.get('name')
        password = request.json.get('password')
        address = request.json.get('address')
        print(email, name, password, address)
        if database.id_duplicate_check(email):
            return jsonify({"message": "중복된 사용자"}), 500, {'Content-Type': 'application/json'}
        else:
            database.addUserInfo(email, name, password, address)
            return jsonify({"message": "성공"}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


# @app.route('/test', methods=["GET"])
# @token_required
# def test(current_user):
#     print(current_user)
#     return jsonify({'message': 'Success'}), 200

# if __name__ == "__main__":
#     app.run(debug = True)
if __name__ == "__main__":
    app.run(host='0.0.0.0')