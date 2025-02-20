# AR_GEE_DB_API 說明文件

## 概述
**AR_GEE_DB_API** 是一個針對 AR GEE 系統資料庫的 API 專案，支援兩個資料庫：
- **ar_gee**：主要用於學生、練習單元、練習統計、練習答案與練習問題的 CRUD 操作。 (暫時沒使用)
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
- [資料庫架構](#資料庫架構)
- [如何使用](#如何使用)
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

3. **進入專案目錄：**
  
   ```bash
   cd AR_GEE_DB_API

4. **安裝相依套件：**

   ```bash
   pip install -r requirements.txt
   
6. **建立資料庫**
   在 MySQL 中匯入兩個資料庫：ar_gee（暫時沒使用） 與 ar_gee_teaching。

## 啟動 API

在專案根目錄下執行以下指令來啟動 Flask 伺服器，系統會自動初始化資料表：
```bash
python app.py
```

## API 端點

詳細參數請直接查看程式碼，有完整說明。

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

## 資料庫架構

### ar_gee

### 1. PracticeAnswers
- **資料表名稱**：practice_answers  
- **綁定鍵**：ar_gee  
- **描述**：儲存練習答案記錄。
- **欄位說明**:
  - `practice_answer_id` (String(255), 主鍵, 非空)：練習答案的唯一識別碼。
  - `student_id` (Text, 非空)：回答者的學生 ID。
  - `practice_question_id` (Text, 非空)：對應的練習題目 ID。
  - `is_correct` (Boolean, 非空)：是否答對。
  - `response_time` (Time, 非空)：回答所花費的時間。
  - `test_date` (DateTime, 非空)：測試日期與時間。
  - `incorrect_attempts` (Integer, 非空)：答錯次數。

### 2. PracticeQuestions
- **資料表名稱**：practice_questions  
- **綁定鍵**：ar_gee  
- **描述**：儲存練習題目記錄。
- **欄位說明**:
  - `practice_question_id` (String(255), 主鍵, 非空)：練習題目的唯一識別碼。
  - `unit_id` (Text, 非空)：所屬單元的 ID。

### 3. PracticeStatistics
- **資料表名稱**：practice_statistics  
- **綁定鍵**：ar_gee  
- **描述**：儲存學生在練習中的統計數據。
- **欄位說明**:
  - `student_id` (Text, 主鍵, 非空)：學生 ID。
  - `unit_id` (Text, 主鍵, 非空)：單元 ID。
  - `total_correct` (Integer, 非空)：答對的題數。
  - `total_questions` (Integer, 非空, 預設值：3)：題目總數。
  - `accuracy_rate` (Float, 非空)：正確率。

### 4. PracticeUnits
- **資料表名稱**：practice_units  
- **綁定鍵**：ar_gee  
- **描述**：儲存練習單元相關資訊。
- **欄位說明**:
  - `unit_id` (String(255), 主鍵, 非空)：單元的唯一識別碼。
  - `unit_name` (Text, 非空)：單元名稱。
  - `video_code` (Text, 非空)：相關影片代碼。

### 5. Students
- **資料表名稱**：students  
- **綁定鍵**：ar_gee  
- **描述**：儲存學生基本資訊（適用於練習模組）。
- **欄位說明**:
  - `student_id` (String(255), 主鍵)：學生的唯一識別碼。
  - `username` (Text, 非空)：使用者名稱。
  - `password` (Text, 非空)：密碼（通常已加密）。
  - `age` (Integer, 非空)：學生年齡。
  - `disorder_category` (Text, 非空)：障礙類別。
  - `created_at` (DateTime, 非空)：資料建立時間。

---

### ar_gee_teaching

### 1. Answers
- **資料表名稱**：answers  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學相關的答案記錄。
- **欄位說明**:
  - `answer_id` (String(255), 主鍵)：答案的唯一識別碼。
  - `student_id` (Text, 非空)：學生 ID。
  - `question_id` (Text, 非空)：對應題目 ID。
  - `is_correct` (Boolean, 非空)：答案是否正確。
  - `response_time` (Time, 非空)：回答所花費的時間。
  - `test_date` (DateTime, 非空)：測試日期與時間。
  - `incorrect_attempts` (Integer, 非空)：答錯次數。

### 2. Questions
- **資料表名稱**：questions  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學問題記錄。
- **欄位說明**:
  - `question_id` (String(255), 主鍵)：問題的唯一識別碼。
  - `unit_id` (Text, 非空)：所屬單元 ID。

### 3. Statistics
- **資料表名稱**：statistics  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學統計資料。
- **欄位說明**:
  - `student_id` (Text, 主鍵, 非空)：學生 ID。
  - `unit_id` (Text, 主鍵, 非空)：單元 ID。
  - `total_correct` (Integer, 非空)：答對的題數。
  - `total_questions` (Integer, 非空, 預設值：3)：題目總數。
  - `accuracy_rate` (Float, 非空)：正確率。

### 4. TcStudents
- **資料表名稱**：students  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學用學生的基本資訊。
- **欄位說明**:
  - `student_id` (String(255), 主鍵)：學生的唯一識別碼。
  - `name` (Text, 非空)：學生姓名。
  - `gender` (Enum('男性', '女性', '其他', ''), 非空)：性別。
  - `birth_date` (Date, 非空)：出生日期。
  - `age` (Integer, 非空)：年齡。
  - `disorder_category` (Text, 非空)：障礙類別。
  - `created_at` (DateTime, 非空)：建立時間。

### 5. Units
- **資料表名稱**：units  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學單元資訊。
- **欄位說明**:
  - `unit_id` (String(255), 主鍵)：單元的唯一識別碼。
  - `unit_name` (Text, 非空)：單元名稱。
  - `video_code` (Text, 非空)：影片代碼。

### 6. Users
- **資料表名稱**：users  
- **綁定鍵**：ar_gee_teaching  
- **描述**：儲存教學系統的使用者帳號資訊。
- **欄位說明**:
  - `user_id` (String(255), 主鍵)：用戶的唯一識別碼。
  - `student_id` (Text, 非空)：關聯學生 ID。
  - `username` (Text, 非空)：使用者名稱。
  - `password` (Text, 非空)：密碼（已加密）。
  - `role` (Text, 非空)：使用者角色。
  - `created_at` (DateTime, 非空)：帳號建立時間。

## 如何使用

1. 啟動 API
- 確保已依照 [安裝與設定] 部分準備好環境與資料庫。
- 在專案根目錄下執行以下命令以啟動 Flask 伺服器：

```bash
python app.py
```

- 預設伺服器會在 http://localhost:5000 執行。

2. 您可以使用各種 HTTP 客戶端工具（例如 curl、Postman 或直接在瀏覽器中）來與 API 互動。

**範例 - 查詢所有學生資料**
- HTTP GET 請求

```bash
curl -X GET http://[yourip]:5000/students
```

**範例 - 新增學生資料**

```bash
curl -X POST http://[yourip]:5000/students \
     -H "Content-Type: application/json" \
     -d '{"username": "john_doe", "age": 20, "disorder_category": "None"}'
```

**範例 - 更新學生資料**

```bash
curl -X PUT http://[yourip]]:5000/students/student_abcdefgh \
     -H "Content-Type: application/json" \
     -d '{"username": "john_updated", "age": 21}'
```

**範例 - 刪除學生資料**

```bash
curl -X DELETE http://[yourip]:5000/students/student_abcdefgh
```
