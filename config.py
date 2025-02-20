"""
config.py 模組

此模組定義了資料庫連線的配置參數，
包含資料庫使用者、主機位址以及 SQLAlchemy 的連線設定。

配置參數說明：
- DB_USER: 資料庫使用者名稱
- DB_HOST: 資料庫主機位址
- SQLALCHEMY_BINDS: 定義多個資料庫的連線 URI，
    分別綁定到 "ar_gee" 與 "ar_gee_teaching" 兩個資料庫
- SQLALCHEMY_TRACK_MODIFICATIONS: 設為 False 以停用物件追蹤，提高效能
"""

DB_USER = "root"
DB_HOST = "localhost"

SQLALCHEMY_BINDS = {
    "ar_gee": f"mysql+pymysql://{DB_USER}@{DB_HOST}/ar_gee",
    "ar_gee_teaching": f"mysql+pymysql://{DB_USER}@{DB_HOST}/ar_gee_teaching"
}

SQLALCHEMY_TRACK_MODIFICATIONS = False
