from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    # 1) 기본 설정(클래스) 로드
    app.config.from_object("src.config.DevelopmentConfig")
    # 2) instance/config.py (또는 .env) 로부터 추가 설정 덮어쓰기
    app.config.from_pyfile("../instance/config.py", silent=True)

    # 확장 모듈 초기화
    db.init_app(app)
    migrate.init_app(app, db)
    # 템플릿+정적 파일에서 API 호출 시 CORS 허용
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 3) Blueprint 등록 (API + 뷰 페이지)
    from src.routes import register_routes
    register_routes(app)

    return app
