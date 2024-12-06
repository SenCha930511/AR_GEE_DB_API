import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Users
from models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users_bp', __name__)

# 取得所有用戶資料
@users_bp.route("/users", methods=["GET"])
def get_users():
    users = Users.query.all()
    users_data = [
        {
            "user_id": user.user_id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for user in users
    ]
    return jsonify(users_data)

# 取得單一用戶資料
@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_data = {
        "user_id": user.user_id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(user_data)

# 新增用戶資料
@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json

    if not data.get("username") or not data.get("password") or not data.get("role"):
        return jsonify({"error": "Missing required fields"}), 400

    # 生成唯一 user_id
    generated_user_id = f"user_{uuid.uuid4().hex[:8]}"

    # 將密碼加密
    hashed_password = generate_password_hash(data.get("password"))

    # 設定創建時間
    created_at = datetime.now()

    # 創建新用戶
    user = Users(
        user_id=generated_user_id,
        username=data.get("username"),
        password=hashed_password,
        role=data.get("role"),
        created_at=created_at
    )

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully", "user_id": generated_user_id}), 201

# 更新用戶資料
@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    # 更新用戶名
    user.username = data.get("username", user.username)

    # 如果有提供密碼，則更新並加密
    if data.get("password"):
        user.password = generate_password_hash(data.get("password"))

    # 更新角色
    user.role = data.get("role", user.role)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})

# 刪除用戶資料
@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# 驗證用戶密碼
@users_bp.route("/users/authenticate", methods=["POST"])
def authenticate_user():
    data = request.json

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    user = Users.query.filter_by(username=data.get("username")).first()
    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({"message": "Authentication successful", "user_id": user.user_id})
