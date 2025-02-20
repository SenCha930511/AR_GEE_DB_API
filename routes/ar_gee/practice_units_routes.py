from flask import Blueprint, request, jsonify
from models.ar_gee_model import PracticeUnits
from models import db

# 定義 Blueprint
practice_unit_bp = Blueprint("practice_unit_bp", __name__)

@practice_unit_bp.route("/practice_units", methods=["POST"])
def add_practice_unit():
    """
    新增練習單元資料

    從請求 JSON 中解析練習單元資料，檢查必填欄位 (unit_id, unit_name, video_code)，
    建立新的練習單元記錄並儲存至資料庫。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201；若缺少必填欄位則回傳錯誤訊息與 HTTP 狀態碼 400
    """
    data = request.json

    # 檢查必填欄位
    required_fields = ["unit_id", "unit_name", "video_code"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_unit = PracticeUnits(
        unit_id=data["unit_id"],
        unit_name=data["unit_name"],
        video_code=data["video_code"]
    )
    db.session.add(new_unit)
    db.session.commit()
    return jsonify({"message": "Practice unit added successfully"}), 201


@practice_unit_bp.route("/practice_units", methods=["GET"])
def get_practice_units():
    """
    查詢所有練習單元資料

    從資料庫中查詢所有練習單元記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有練習單元資料的 JSON 列表
    """
    units = PracticeUnits.query.all()
    unit_list = [{
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    } for unit in units]
    return jsonify(unit_list)


@practice_unit_bp.route("/practice_units/<unit_id>", methods=["GET"])
def get_practice_unit(unit_id: str):
    """
    根據 unit_id 查詢特定練習單元

    根據 unit_id 從資料庫中查詢單一練習單元記錄。

    :param unit_id: str - 練習單元 ID
    :return: jsonify - 回傳該單元的 JSON 格式資料；若查無資料則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404
    unit_data = {
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    }
    return jsonify(unit_data)


@practice_unit_bp.route("/practice_units/<unit_id>", methods=["PUT"])
def update_practice_unit(unit_id: str):
    """
    更新練習單元資料

    根據 unit_id 更新練習單元記錄，若查無該記錄則回傳錯誤訊息。

    :param unit_id: str - 練習單元 ID
    :return: jsonify - 回傳更新成功訊息；若查無該記錄則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404

    data = request.json
    unit.unit_name = data.get("unit_name", unit.unit_name)
    unit.video_code = data.get("video_code", unit.video_code)

    db.session.commit()
    return jsonify({"message": "Practice unit updated successfully"})


@practice_unit_bp.route("/practice_units/<unit_id>", methods=["DELETE"])
def delete_practice_unit(unit_id: str):
    """
    刪除練習單元資料

    根據 unit_id 刪除練習單元記錄，若查無該記錄則回傳錯誤訊息。

    :param unit_id: str - 練習單元 ID
    :return: jsonify - 回傳刪除成功訊息；若查無該記錄則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = PracticeUnits.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Practice unit not found"}), 404

    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Practice unit deleted successfully"})
