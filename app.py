"""
AR_GEE_DB_API Flask 應用程式

此模組負責初始化並啟動 AR_GEE_DB_API 的 Flask 應用程式，包含以下功能：
- 建立 Flask 應用程式實例
- 設定多資料庫連線資訊
- 初始化 SQLAlchemy
- 註冊各個 API 模組 (Blueprints)
- 啟動應用程式伺服器

使用方式:
    直接執行此模組以啟動應用程式伺服器。
"""

from flask import Flask
from models import db
from routes.ar_gee import (
    student_bp,
    practice_unit_bp,
    practice_statistics_bp,
    practice_answers_bp,
    practice_questions_bp
)
from routes.ar_gee_teaching import (
    answers_bp,
    questions_bp,
    statistics_bp,
    tc_students_bp,
    units_bp,
    users_bp
)
from config import SQLALCHEMY_BINDS, SQLALCHEMY_TRACK_MODIFICATIONS


def create_app() -> Flask:
    """
    建立並設定 Flask 應用程式。

    此函數完成以下操作：
    - 初始化 Flask 應用
    - 設定多資料庫連線資訊 (SQLALCHEMY_BINDS 與 SQLALCHEMY_TRACK_MODIFICATIONS)
    - 初始化 SQLAlchemy
    - 註冊各個 Blueprint 模組

    :return: Flask - 已配置的 Flask 應用程式實例
    """
    app: Flask = Flask(__name__)

    # 設定多資料庫連線資訊
    app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

    # 初始化 SQLAlchemy
    db.init_app(app)

    # 定義 Blueprint 列表
    blueprints = [
        student_bp,
        practice_unit_bp,
        practice_statistics_bp,
        practice_answers_bp,
        practice_questions_bp,
        answers_bp,
        questions_bp,
        statistics_bp,
        tc_students_bp,
        units_bp,
        users_bp
    ]

    # 註冊所有 Blueprint
    for blueprint in blueprints:
        app.register_blueprint(blueprint)

    return app


if __name__ == "__main__":
    """
    主程式區塊：
    - 建立 Flask 應用程式實例
    - 在應用程式上下文中建立資料庫資料表
    - 啟動 Flask 應用程式 (除錯模式)
    """
    app: Flask = create_app()
    with app.app_context():
        # 創建 ar_gee 資料庫的資料表
        db.create_all("ar_gee")
        # 創建 ar_gee_teaching 資料庫的資料表
        db.create_all("ar_gee_teaching")
    # 以除錯模式啟動應用程式伺服器
    app.run(debug=True)
