import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Users
from models import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 定義 Blueprint
users_bp = Blueprint('users_bp', __name__)

@users_bp.route("/users", methods=["GET"])
def get_users():
    """
    取得所有用戶資料

    從資料庫中查詢所有用戶記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有用戶資料的 JSON 列表
    """
    users = Users.query.all()
    users_data = [
        {
            "user_id": user.user_id,
            "student_id": user.student_id,
            "username": user.username,
            "role": user.role,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        for user in users
    ]
    return jsonify(users_data)


@users_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id: str):
    """
    取得單一用戶資料

    根據 user_id 查詢單一用戶記錄。

    :param user_id: str - 用戶 ID
    :return: jsonify - 回傳該用戶的 JSON 格式資料；若查無用戶則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user_data = {
        "user_id": user.user_id,
        "student_id": user.student_id,
        "username": user.username,
        "role": user.role,
        "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(user_data)


@users_bp.route("/users", methods=["POST"])
def create_user():
    """
    新增用戶資料

    從請求 JSON 中解析用戶資料，檢查必填欄位與 username 重複性，
    生成唯一的 user_id，將密碼加密後建立新用戶記錄，並儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201；若缺少必填欄位或 username 重複則回傳錯誤訊息與 HTTP 狀態碼 400
    """
    data = request.json

    # 檢查必填欄位是否存在
    if not data.get("username") or not data.get("password") or not data.get("role"):
        return jsonify({"error": "Missing required fields"}), 400

    # 檢查資料庫中是否已存在相同的 username
    existing_user = Users.query.filter_by(username=data.get("username")).first()
    if existing_user:
        return jsonify({"error": "Username already exists"}), 400

    # 生成唯一 user_id
    generated_user_id: str = f"user_{uuid.uuid4().hex[:8]}"

    # 將密碼加密
    hashed_password: str = generate_password_hash(data.get("password"))

    # 設定創建時間
    created_at: datetime = datetime.now()

    # 建立新用戶記錄
    user: Users = Users(
        user_id=generated_user_id,
        student_id=data.get("student_id"),
        username=data.get("username"),
        password=hashed_password,
        role=data.get("role"),
        created_at=created_at
    )

    # 將新用戶加入資料庫並提交
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": generated_user_id}), 201


@users_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id: str):
    """
    更新用戶資料

    根據 user_id 更新用戶記錄。若提供 new_password 則需驗證 old_password，
    更新用戶名稱、密碼及角色。

    :param user_id: str - 用戶 ID
    :return: Tuple[jsonify, int] - 回傳更新成功訊息與 HTTP 狀態碼 200；若查無用戶或驗證失敗則回傳錯誤訊息與相應 HTTP 狀態碼
    """
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.json

    # 更新用戶名稱
    user.username = data.get("username", user.username)

    # 如果有提供新密碼，則需要驗證舊密碼是否正確
    if data.get("new_password") and data.get("old_password"):
        if not check_password_hash(user.password, data.get("old_password")):
            return jsonify({"error": "Old password is incorrect"}), 400
        # 更新密碼並加密
        user.password = generate_password_hash(data.get("new_password"))

    # 更新角色
    user.role = data.get("role", user.role)

    db.session.commit()
    return jsonify({"message": "User updated successfully"})


@users_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id: str):
    """
    刪除用戶資料

    根據 user_id 刪除用戶記錄。

    :param user_id: str - 用戶 ID
    :return: Tuple[jsonify, int] - 回傳刪除成功訊息與 HTTP 狀態碼 200；若查無用戶則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    user = Users.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})


@users_bp.route("/users/authenticate", methods=["POST"])
def authenticate_user():
    """
    驗證用戶密碼

    根據提供的 username 與 password 驗證用戶身份。
    若驗證成功，回傳用戶基本資料；否則回傳錯誤訊息。

    :return: Tuple[jsonify, int] - 回傳驗證結果與相應的 HTTP 狀態碼；若缺少欄位則回傳錯誤訊息與 HTTP 狀態碼 400，若驗證失敗則回傳錯誤訊息與 HTTP 狀態碼 401
    """
    data = request.json

    if not data.get("username") or not data.get("password"):
        return jsonify({"error": "Missing username or password"}), 400

    user = Users.query.filter_by(username=data.get("username")).first()
    if not user or not check_password_hash(user.password, data.get("password")):
        return jsonify({"error": "Invalid username or password"}), 401

    return jsonify({
        "message": "Authentication successful",
        "user_id": user.user_id,
        "role": user.role,
        "student_id": user.student_id
    })
