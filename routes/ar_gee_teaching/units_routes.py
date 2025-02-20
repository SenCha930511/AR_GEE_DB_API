import uuid
from flask import Blueprint, request, jsonify
from models.ar_gee_teaching_model import Units
from models import db

# 定義 Blueprint
units_bp = Blueprint('units_bp', __name__)

@units_bp.route("/units", methods=["GET"])
def get_units():
    """
    取得所有單元資料

    從資料庫中查詢所有單元記錄，並以 JSON 列表格式回傳。

    :return: jsonify - 回傳所有單元資料的 JSON 列表
    """
    units = Units.query.all()
    units_data = [
        {
            "unit_id": unit.unit_id,
            "unit_name": unit.unit_name,
            "video_code": unit.video_code
        }
        for unit in units
    ]
    return jsonify(units_data)


@units_bp.route("/units/<unit_id>", methods=["GET"])
def get_unit(unit_id: str):
    """
    取得單一單元資料

    根據 unit_id 查詢單一單元記錄。

    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳該單元的 JSON 格式資料；若查無單元則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404
    unit_data = {
        "unit_id": unit.unit_id,
        "unit_name": unit.unit_name,
        "video_code": unit.video_code
    }
    return jsonify(unit_data)


@units_bp.route("/units", methods=["POST"])
def create_unit():
    """
    新增單元資料

    從請求 JSON 中取得單元資料，生成唯一的 unit_id，建立並儲存新的單元記錄。

    :return: Tuple[jsonify, int] - 回傳成功訊息與 HTTP 狀態碼 201
    """
    data = request.json
    
    # 生成唯一的 unit_id
    generated_unit_id: str = f"unit_{uuid.uuid4().hex[:8]}"
    
    unit = Units(
        unit_id=generated_unit_id,
        unit_name=data.get("unit_name"),
        video_code=data.get("video_code")
    )
    db.session.add(unit)
    db.session.commit()
    return jsonify({"message": "Unit created successfully", "unit_id": generated_unit_id}), 201


@units_bp.route("/units/<unit_id>", methods=["PUT"])
def update_unit(unit_id: str):
    """
    更新單元資料

    根據 unit_id 更新單元記錄。若查無該單元則回傳錯誤訊息。

    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳更新成功訊息；若查無該單元則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    data = request.json
    unit.unit_name = data.get("unit_name", unit.unit_name)
    unit.video_code = data.get("video_code", unit.video_code)

    db.session.commit()
    return jsonify({"message": "Unit updated successfully"})


@units_bp.route("/units/<unit_id>", methods=["DELETE"])
def delete_unit(unit_id: str):
    """
    刪除單元資料

    根據 unit_id 刪除單元記錄。若查無該單元則回傳錯誤訊息。

    :param unit_id: str - 單元 ID
    :return: jsonify - 回傳刪除成功訊息；若查無該單元則回傳錯誤訊息與 HTTP 狀態碼 404
    """
    unit = Units.query.get(unit_id)
    if not unit:
        return jsonify({"error": "Unit not found"}), 404

    db.session.delete(unit)
    db.session.commit()
    return jsonify({"message": "Unit deleted successfully"})
