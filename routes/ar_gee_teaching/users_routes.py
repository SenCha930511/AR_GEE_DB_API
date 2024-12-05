from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Users
from models import db

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
    user = Users(
        user_id=data.get("user_id"),
        username=data.get("username"),
        password=data.get("password"),
        role=data.get("role"),
        created_at=data.get("created_at")
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created successfully"}), 201

# 更新用戶資料
@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    user.username = data.get("username", user.username)
    user.password = data.get("password", user.password)
    user.role = data.get("role", user.role)
    user.created_at = data.get("created_at", user.created_at)

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
