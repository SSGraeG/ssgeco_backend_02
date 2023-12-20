from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps
import database
import modeling
import datetime
from os import path
import os
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

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
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/', methods=['GET'])
def main():
    # sort = request.args.get('sort')
    # keyword = request.args.get('keyword')
    # return database.getItems(sort, keyword)
    return database.get_all()


@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        is_id = database.id_check(email, password)
        if is_id:
            token = create_access_token(identity=email, expires_delta=datetime.timedelta(seconds=100))
            authenticated_users[token] = email
            return jsonify({'token': token}), 200
        else:
            return jsonify({'message': '잘못된 로그인 정보'}), 401


@app.route('/logout', methods=["GET"])
@token_required
def logout(current_user):
    token = request.headers.get('x-access-token')
    if token in authenticated_users:
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

        if database.id_duplicate_check(email):
            return jsonify({"message": "중복된 사용자"}), 500, {'Content-Type': 'application/json'}
        else:
            database.sign_up(email, name, password, address)
            return jsonify({"message": "성공"}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


@app.route('/mypage', methods=["GET"])
@token_required
def mypage(current_user):
    try:
        return database.get_user(current_user)
    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}


# @app.route('/image', methods=["POST"])
# # @token_required
# def image():
#     try:
#         # file = request.files['image']
#         # filename = file.filename
#         # print(file, filename)
#         # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         file = request.files['image']
#
#         np.set_printoptions(suppress=True)
#
#         # Load the model
#         model = load_model("keras_Model.h5", compile=False)
#
#         # Load the labels
#         class_names = open("labels.txt", "r").readlines()
#
#         # Create the array of the right shape to feed into the keras model
#         # The 'length' or number of images you can put into the array is
#         # determined by the first position in the shape tuple, in this case 1
#         data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
#
#         # Replace this with the path to your image
#         # image = Image.open("<IMAGE_PATH>").convert("RGB")
#         image = Image.open(file.stream).convert("RGB")
#         # resizing the image to be at least 224x224 and then cropping from the center
#         size = (224, 224)
#         image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
#
#         # turn the image into a numpy array
#         image_array = np.asarray(image)
#
#         # Normalize the image
#         normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
#
#         # Load the image into the array
#         data[0] = normalized_image_array
#
#         # Predicts the model
#         prediction = model.predict(data)
#         index = np.argmax(prediction)
#         class_name = class_names[index]
#         confidence_score = prediction[0][index]
#
#         # Print prediction and confidence score
#         print("Class:", class_name[2:], end="")
#         print("Confidence Score:", confidence_score)
#         return jsonify({"message": "성공"}), 200, {'Content-Type': 'application/json'}
#     except Exception as e:
#         print(e)
#         return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}

@app.route('/image', methods=["POST"])
# @token_required
def image():
    try:
        file = request.files['image']
        result = modeling.predict_image(file)
        if result == "wash":
            return jsonify({"message": "성공ㅇㅇ"}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"message": "실패"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}

# if __name__ == "__main__":
#     app.run(debug = True)
if __name__ == "__main__":
    app.run(host='0.0.0.0')