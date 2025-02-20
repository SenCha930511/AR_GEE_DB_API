# AR_GEE_DB_API 說明文件

## 概述
**AR_GEE_DB_API** 是一個針對 AR GEE 系統資料庫的 API 專案，支援兩個資料庫：
- **ar_gee**：主要用於學生、練習單元、練習統計、練習答案與練習問題的 CRUD 操作。
- **ar_gee_teaching**：用於教學相關的資料，如答案、問題、統計、學生、單元與使用者管理。

此 API 採用 [Flask](https://flask.palletsprojects.com/) 與 [SQLAlchemy](https://www.sqlalchemy.org/) 來建構與管理資料庫連線。

---

## 目錄
- [前置需求](#前置需求)
- [安裝與設定](#安裝與設定)
- [啟動 API](#啟動-api)
- [API 端點](#api-端點)
  - [ar_gee 相關端點](#ar_gee-相關端點)
  - [ar_gee_teaching 相關端點](#ar_gee_teaching-相關端點)
---

## 前置需求
- Python 3.x
- MySQL Server
- pip（Python 套件管理工具）

---

## 安裝與設定

1. **Clone 專案：**
   ```bash
   git clone https://github.com/SenCha930511/AR_GEE_DB_API.git

2. **進入專案目錄：**
   ```bash
   cd AR_GEE_DB_API

3. **安裝相依套件：**
   ```bash
   pip install -r requirements.txt
   
4. **建立資料庫**
   在 MySQL 中匯入兩個資料庫：ar_gee（暫時沒使用） 與 ar_gee_teaching。

## 啟動 API

在專案根目錄下執行以下指令來啟動 Flask 伺服器，系統會自動初始化資料表：
```bash
python app.py
```

## API 端點

本 API 透過多個 Blueprint 進行模組化管理。各個 Blueprint 的簡要介紹如下：

- ar_gee 相關端點（暫時沒使用）
1. student_bp：處理學生相關的 CRUD 操作。
2. practice_unit_bp：處理練習單元相關操作。
3. practice_statistics_bp：處理練習統計資料。
4. practice_answers_bp：處理練習答案。
5. practice_questions_bp：處理練習問題。

- ar_gee_teaching 相關端點
1. answers_bp：處理教學答案相關操作。
2. questions_bp：處理練習問題資料。
3. statistics_bp：處理教學統計資料。
4. tc_students_bp：處理教學學生資料。
5. units_bp：處理教學單元操作
6. users_bp：處理使用者管理。
