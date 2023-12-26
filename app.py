from flask import Flask
from flask_cors import CORS
from routes.user import user_bp
from routes.modeling import model_bp
from routes.mileage import mileage_bp
from routes.mypage import mypage_bp
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__, static_folder='./resources/')
    app.config["JWT_SECRET_KEY"] = "super-secret"

    # app.authenticated_users = {}

    # Blueprint 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(model_bp)
    app.register_blueprint(mileage_bp)
    app.register_blueprint(mypage_bp)

    # CORS 설정
    CORS(app, resources={r"/*": {"origins": "*"}})

    # JWTManager 초기화
    jwt = JWTManager(app)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
