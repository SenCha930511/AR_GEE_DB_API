from flask import Flask
from models import db
from routes.ar_gee import student_bp, practice_unit_bp, practice_statistics_bp, practice_answers_bp, practice_questions_bp
from config import SQLALCHEMY_BINDS, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)

# 設定多資料庫
app.config["SQLALCHEMY_BINDS"] = SQLALCHEMY_BINDS
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS

db.init_app(app)  # 初始化 SQLAlchemy

# 定義 Blueprint 列表
blueprints = [
    student_bp,
    practice_unit_bp,
    practice_statistics_bp,
    practice_answers_bp,
    practice_questions_bp
]

# 註冊所有 Blueprint
for blueprint in blueprints:
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    with app.app_context():
        db.create_all("ar_gee")  # 創建 ar_gee 資料庫的資料表
        # db.create_all("ar_gee_teaching") # 創建 ar_gee_teaching 資料庫的資料表
    app.run(debug=True)
