from flask import Blueprint, request, jsonify, Flask
from functools import wraps
from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from authenticated_users import authenticated_users
from . import database_api as database
from flask import Flask

app = Flask(__name__)
model_bp = Blueprint('model_bp', __name__)

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
        app.logger.debug(current_user)
        return f(current_user, *args, **kwargs)

    return decorated


def predict_image(file):
    try:
        np.set_printoptions(suppress=True)

        # Load the model
        model = load_model("/home/ubuntu/ssg_backend/keras_model.h5", compile=False)

        # Load the labels
        class_names = open("/home/ubuntu/ssg_backend/labels.txt", "r").readlines()

        # Create the array of the right shape to feed into the keras model
        # The 'length' or number of images you can put into the array is
        # determined by the first position in the shape tuple, in this case 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

        # Replace this with the path to your image
        # image = Image.open("<IMAGE_PATH>").convert("RGB")
        image = Image.open(file.stream).convert("RGB")
        # resizing the image to be at least 224x224 and then cropping from the center
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

        # turn the image into a numpy array
        image_array = np.asarray(image)

        # Normalize the image
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

        # Load the image into the array
        data[0] = normalized_image_array

        # Predicts the model
        prediction = model.predict(data)
        index = np.argmax(prediction)
        class_name = class_names[index]
        confidence_score = prediction[0][index]

        # app.logger.debug prediction and confidence score
        app.logger.debug("Class:", class_name[2:])
        app.logger.debug("Confidence Score:", confidence_score)
        return class_name[2:]
    except Exception as e:
        app.logger.debug(e)




@model_bp.route('/image', methods=["POST"])
@token_required
def image(current_user):
    try:
        file = request.files['image']
        result = predict_image(file)

        if result.rstrip() == "wash":
            current_mileage = database.add_mileage(current_user)
            return jsonify({"message": "성공", "mileage": current_mileage}), 200, {'Content-Type': 'application/json'}
        else:
            return jsonify({"message": "실패"}), 200, {'Content-Type': 'application/json'}
    except Exception as e:
        app.logger.debug(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
