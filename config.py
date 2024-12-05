# config.py

DB_USER = "root"
DB_HOST = "localhost"

SQLALCHEMY_BINDS = {
    "ar_gee": f"mysql+pymysql://{DB_USER}@{DB_HOST}/ar_gee",
    "ar_gee_teaching": f"mysql+pymysql://{DB_USER}@{DB_HOST}/ar_gee_teaching"
}

SQLALCHEMY_TRACK_MODIFICATIONS = False