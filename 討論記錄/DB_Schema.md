# 測驗系統資料庫設計文件 v1.0

## 📋 專案概述

本文件描述測驗系統的完整資料庫架構，支援四種題型（閱讀、字彙、聽力、口說）的線上測驗平台。

### 技術規格

- **資料庫**: MariaDB 11.3+
- **字符集**: utf8mb4
- **排序規則**: utf8mb4_unicode_ci
- **引擎**: InnoDB
- **支援語言**: 繁體中文

---

## 🗄️ 資料表結構

### 1. 使用者管理 (users)

管理系統中的所有使用者帳戶資訊。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 使用者內部 ID（遞增） |
| email | VARCHAR(255) | UNIQUE, NOT NULL | 電子郵件地址 |
| password | VARCHAR(255) | NOT NULL | 密碼雜湊值 |
| nickname | VARCHAR(255) | | 使用者暱稱 |
| role | VARCHAR(255) | DEFAULT 'user' | 使用者角色 |
| is_active | BOOLEAN | DEFAULT TRUE | 帳號啟用狀態 |
| last_login_at | TIMESTAMP | | 最後登入時間 |
| point | INT | DEFAULT 0 | 使用者積分 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 更新時間 |

**索引**:
- `idx_email` (email)
- `idx_nickname` (nickname)
- `idx_role` (role)
- `idx_active` (is_active)

### 2. 題目分類 (question_categories)

階層式題目分類系統，支援巢狀分類。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 分類 ID |
| name | VARCHAR(100) | NOT NULL | 分類名稱 |
| description | TEXT | | 分類描述 |
| parent_id | BIGINT UNSIGNED | FK | 父分類 ID |
| sort_order | INT | DEFAULT 0 | 排序順序 |
| is_active | BOOLEAN | DEFAULT TRUE | 分類狀態 |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 更新時間 |

**外鍵**: `parent_id` → `question_categories(id)`

### 3. 題目主表 (questions)

統一存放所有類型題目，使用 JSON 格式存放題目內容。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 題目 ID |
| category_id | BIGINT UNSIGNED | FK, NOT NULL | 所屬分類 ID |
| type | ENUM | NOT NULL | 題目類型 |
| title | VARCHAR(500) | NOT NULL | 題目標題 |
| content | JSON | NOT NULL | 題目內容與資源 |
| difficulty_level | TINYINT | DEFAULT 1 | 難度等級 (1-5) |
| points | DECIMAL(5,2) | DEFAULT 1.00 | 題目分數 |
| time_limit | INT | | 單題時間限制(秒) |
| explanation | TEXT | | 解題說明 |
| tags | JSON | | 標籤陣列 |
| **has_media** | BOOLEAN | **Generated Column** | **自動檢測是否包含媒體** |
| **has_images** | BOOLEAN | **Generated Column** | **自動檢測是否包含圖片** |
| **has_audio** | BOOLEAN | **Generated Column** | **自動檢測是否包含音訊** |
| **has_video** | BOOLEAN | **Generated Column** | **自動檢測是否包含影片** |
| **option_count** | TINYINT | **Generated Column** | **自動計算選項數量** |
| status | ENUM | DEFAULT 'draft' | 題目狀態 |
| created_by | BIGINT UNSIGNED | FK, NOT NULL | 建立者 ID |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 更新時間 |

**題目類型**: `reading` | `vocab` | `listen` | `speak`  
**題目狀態**: `draft` | `active` | `archived`

**外鍵**:
- `category_id` → `question_categories(id)`
- `created_by` → `users(id)`

### 4. 測驗模板 (exam_templates)

定義測驗的結構、規則和設定。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 模板 ID |
| name | VARCHAR(200) | NOT NULL | 測驗名稱 |
| description | TEXT | | 測驗描述 |
| instructions | TEXT | | 測驗說明 |
| category_id | BIGINT UNSIGNED | FK | 模板分類 |
| total_time_limit | INT | | 總時間限制(分鐘) |
| passing_score | DECIMAL(5,2) | DEFAULT 60.00 | 及格分數(%) |
| max_attempts | TINYINT | DEFAULT 1 | 最大嘗試次數 |
| shuffle_questions | BOOLEAN | DEFAULT FALSE | 隨機題目順序 |
| shuffle_options | BOOLEAN | DEFAULT FALSE | 隨機選項順序 |
| show_results_immediately | BOOLEAN | DEFAULT TRUE | 立即顯示結果 |
| allow_review | BOOLEAN | DEFAULT TRUE | 允許檢閱答案 |
| allow_backtrack | BOOLEAN | DEFAULT TRUE | 允許返回前題 |
| is_public | BOOLEAN | DEFAULT FALSE | 公開測驗 |
| start_time | TIMESTAMP | | 開放開始時間 |
| end_time | TIMESTAMP | | 開放結束時間 |
| created_by | BIGINT UNSIGNED | FK, NOT NULL | 建立者 ID |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 建立時間 |
| updated_at | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | 更新時間 |

### 5. 測驗題目關聯 (exam_questions)

定義測驗包含哪些題目及其順序。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 關聯 ID |
| exam_template_id | BIGINT UNSIGNED | FK, NOT NULL | 測驗模板 ID |
| question_id | BIGINT UNSIGNED | FK, NOT NULL | 題目 ID |
| question_order | INT | NOT NULL | 題目順序 |
| points_override | DECIMAL(5,2) | | 覆蓋預設分數 |
| is_required | BOOLEAN | DEFAULT TRUE | 是否為必答題 |

**唯一約束**: `unique_exam_question` (exam_template_id, question_id)

### 6. 測驗執行 (exam_sessions)

記錄使用者的測驗執行狀態和過程。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 會話 ID |
| exam_template_id | BIGINT UNSIGNED | FK, NOT NULL | 測驗模板 ID |
| user_id | BIGINT UNSIGNED | FK, NOT NULL | 使用者 ID |
| session_token | VARCHAR(64) | UNIQUE, NOT NULL | 會話令牌 |
| attempt_number | TINYINT | DEFAULT 1 | 嘗試次數 |
| status | ENUM | DEFAULT 'not_started' | 會話狀態 |
| started_at | TIMESTAMP | | 開始時間 |
| completed_at | TIMESTAMP | | 完成時間 |
| expired_at | TIMESTAMP | | 過期時間 |
| time_remaining | INT | | 剩餘時間(秒) |
| current_question_index | INT | DEFAULT 0 | 當前題目索引 |
| total_questions | INT | DEFAULT 0 | 總題目數 |
| answered_questions | INT | DEFAULT 0 | 已答題目數 |
| total_score | DECIMAL(8,2) | DEFAULT 0 | 總得分 |
| max_possible_score | DECIMAL(8,2) | | 最高可能分數 |
| percentage_score | DECIMAL(5,2) | | 百分比分數 |
| passed | BOOLEAN | | 是否通過 |
| browser_info | JSON | | 瀏覽器資訊 |
| ip_address | VARCHAR(45) | | IP 位址 |

**會話狀態**: `not_started` | `in_progress` | `completed` | `expired` | `cancelled`

### 7. 答題記錄 (user_answers)

記錄使用者對每個題目的詳細答題資訊。

| 欄位名 | 資料型別 | 約束 | 說明 |
|--------|----------|------|------|
| id | BIGINT UNSIGNED | PK, AUTO_INCREMENT | 答案 ID |
| session_id | BIGINT UNSIGNED | FK, NOT NULL | 會話 ID |
| question_id | BIGINT UNSIGNED | FK, NOT NULL | 題目 ID |
| question_order | INT | NOT NULL | 題目在測驗中順序 |
| answer_data | JSON | NOT NULL | 答案資料 |
| is_correct | BOOLEAN | | 是否正確 |
| points_earned | DECIMAL(5,2) | DEFAULT 0 | 獲得分數 |
| max_points | DECIMAL(5,2) | NOT NULL | 該題最高分數 |
| time_spent | INT | DEFAULT 0 | 答題時間(秒) |
| attempt_count | INT | DEFAULT 1 | 嘗試次數 |
| is_flagged | BOOLEAN | DEFAULT FALSE | 標記複習 |
| answered_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 答題時間 |
| graded_at | TIMESTAMP | | 評分時間 |
| graded_by | BIGINT UNSIGNED | FK | 評分者 ID |

**唯一約束**: `unique_session_question` (session_id, question_id)

### 8. 統計分析表

#### 測驗統計 (exam_statistics)
記錄每個測驗模板的統計資料。

#### 題目統計 (question_statistics)  
記錄每個題目的答題統計資料。

---

## 📝 題目類型 JSON 格式規範

### 1. 閱讀理解題 (reading)

```json
{
  "passage": {
    "title": "全球暖化的影響",
    "content": "根據最新研究報告顯示，全球暖化對環境造成了前所未有的影響...",
    "word_count": 350,
    "reading_time": 3
  },
  "questions": [
    {
      "id": 1,
      "question_text": "根據文章內容，全球暖化的主要原因是什麼？",
      "type": "multiple_choice",
      "options": [
        {
          "key": "A",
          "text": "工業污染",
          "is_correct": false
        },
        {
          "key": "B", 
          "text": "溫室氣體排放",
          "is_correct": true
        },
        {
          "key": "C",
          "text": "森林砍伐",
          "is_correct": false
        },
        {
          "key": "D",
          "text": "人口增長",
          "is_correct": false
        }
      ]
    },
    {
      "id": 2,
      "question_text": "請簡述文章中提到的三個主要環境影響。",
      "type": "short_answer",
      "max_words": 100,
      "keywords": ["海平面上升", "極端氣候", "生物多樣性"]
    }
  ],
  "media": {
    "images": ["climate_chart.jpg", "temperature_graph.png"],
    "audio": null,
    "video": null
  },
  "metadata": {
    "source": "Environmental Science Journal",
    "difficulty": "intermediate",
    "estimated_time": 8
  }
}
```

### 2. 字彙測驗 (vocab)

```json
{
  "word": "sophisticated",
  "question_text": "Choose the best definition for the word 'sophisticated':",
  "type": "multiple_choice",
  "options": [
    {
      "key": "A",
      "text": "simple and basic",
      "is_correct": false
    },
    {
      "key": "B",
      "text": "complex and refined",
      "is_correct": true
    },
    {
      "key": "C",
      "text": "old-fashioned",
      "is_correct": false
    },
    {
      "key": "D",
      "text": "easy to understand",
      "is_correct": false
    }
  ],
  "pronunciation": {
    "phonetic": "/səˈfɪstɪkeɪtɪd/",
    "audio_url": "sophisticated_pronunciation.mp3"
  },
  "examples": [
    {
      "sentence": "The restaurant serves sophisticated cuisine.",
      "translation": "這家餐廳提供精緻的料理。"
    },
    {
      "sentence": "She has a sophisticated sense of style.",
      "translation": "她有著精緻的時尚品味。"
    }
  ],
  "word_forms": {
    "noun": "sophistication",
    "adverb": "sophisticatedly",
    "verb": "sophisticate"
  },
  "synonyms": ["refined", "cultured", "elegant", "advanced"],
  "antonyms": ["simple", "crude", "basic", "primitive"],
  "media": {
    "images": ["sophisticated_example.jpg"],
    "audio": ["sophisticated_pronunciation.mp3"],
    "video": null
  },
  "difficulty_level": 4,
  "frequency": "high",
  "tags": ["adjective", "intermediate", "business_english"]
}
```

### 3. 聽力測驗 (listen)

```json
{
  "audio": {
    "main_file": "conversation_hotel_booking.mp3",
    "duration": 120,
    "transcript_available": true,
    "playback_limit": 2
  },
  "scenario": {
    "title": "Hotel Reservation Conversation",
    "description": "A customer calls a hotel to make a reservation",
    "participants": ["Customer", "Hotel Receptionist"],
    "setting": "Phone conversation"
  },
  "questions": [
    {
      "id": 1,
      "question_text": "What type of room does the customer want to book?",
      "type": "multiple_choice",
      "audio_segment": {
        "start_time": 15,
        "end_time": 35
      },
      "options": [
        {
          "key": "A",
          "text": "Single room",
          "is_correct": false
        },
        {
          "key": "B",
          "text": "Double room", 
          "is_correct": true
        },
        {
          "key": "C",
          "text": "Suite",
          "is_correct": false
        },
        {
          "key": "D",
          "text": "Family room",
          "is_correct": false
        }
      ]
    },
    {
      "id": 2,
      "question_text": "Fill in the blank: The customer will arrive on ______.",
      "type": "fill_blank",
      "audio_segment": {
        "start_time": 45,
        "end_time": 55
      },
      "correct_answers": ["March 15th", "March 15", "15th March"],
      "case_sensitive": false
    }
  ],
  "transcript": {
    "full_text": "Receptionist: Good morning, Grand Hotel. How may I help you?\nCustomer: Hi, I'd like to make a reservation for a double room...",
    "timestamps": [
      {
        "start": 0,
        "end": 5,
        "speaker": "Receptionist",
        "text": "Good morning, Grand Hotel. How may I help you?"
      },
      {
        "start": 6,
        "end": 12,
        "speaker": "Customer", 
        "text": "Hi, I'd like to make a reservation for a double room."
      }
    ]
  },
  "media": {
    "images": ["hotel_lobby.jpg"],
    "audio": ["conversation_hotel_booking.mp3"],
    "video": null
  },
  "difficulty_level": 2,
  "accent": "American",
  "speed": "normal",
  "background_noise": "minimal"
}
```

### 4. 口說測驗 (speak)

```json
{
  "task_type": "describe_and_compare",
  "question_text": "Look at these two photos and describe the differences between urban and rural transportation. You have 2 minutes to prepare and 3 minutes to speak.",
  "instructions": {
    "preparation_time": 120,
    "speaking_time": 180,
    "requirements": [
      "Compare the two transportation methods",
      "Discuss advantages and disadvantages", 
      "Give your personal opinion",
      "Use specific examples"
    ]
  },
  "prompts": [
    "What differences can you see between these transportation options?",
    "Which method do you prefer and why?",
    "How might these affect people's daily lives?"
  ],
  "media": {
    "images": ["urban_subway.jpg", "rural_bus.jpg"],
    "audio": ["sample_response.mp3"],
    "video": null
  },
  "evaluation_criteria": {
    "fluency_coherence": {
      "weight": 25,
      "max_score": 5,
      "description": "Natural flow of speech and logical organization"
    },
    "pronunciation": {
      "weight": 25,
      "max_score": 5,
      "description": "Clear pronunciation and appropriate intonation"
    },
    "vocabulary": {
      "weight": 25,
      "max_score": 5,
      "description": "Range and accuracy of vocabulary use"
    },
    "grammar": {
      "weight": 25,
      "max_score": 5,
      "description": "Grammatical accuracy and complexity"
    }
  },
  "sample_responses": {
    "band_5": {
      "audio_file": "sample_band5_response.mp3",
      "transcript": "These two pictures show very different ways of transportation...",
      "feedback": "Good vocabulary range, minor grammatical errors"
    },
    "band_3": {
      "audio_file": "sample_band3_response.mp3", 
      "transcript": "I can see bus and train. Bus is for village...",
      "feedback": "Basic vocabulary, simple sentence structures"
    }
  },
  "recording_settings": {
    "max_duration": 180,
    "format": "mp3",
    "quality": "standard",
    "auto_stop": true
  },
  "difficulty_level": 3,
  "topic_category": "transportation",
  "skills_tested": ["comparison", "description", "opinion_expression"]
}
```

---

## 🔍 答題記錄 JSON 格式

### 選擇題答案
```json
{
  "selected_options": ["B"],
  "confidence_level": 4,
  "time_spent": 25,
  "review_flagged": false,
  "answer_changed": 1
}
```

### 填空題答案
```json
{
  "answers": [
    {
      "blank_id": 1,
      "text": "sophisticated",
      "confidence": 5
    }
  ],
  "time_spent": 45,
  "hints_used": 0
}
```

### 口說題答案
```json
{
  "recording": {
    "file_path": "user_123_session_456_q7.mp3",
    "duration": 165,
    "file_size": 2048576,
    "upload_time": "2025-01-15T10:30:00Z"
  },
  "preparation_time_used": 118,
  "speaking_time_used": 165,
  "self_assessment": {
    "difficulty": 3,
    "satisfaction": 4,
    "confidence": 3
  },
  "technical_issues": null,
  "retake_count": 0
}
```

---

## 📊 效能優化特性

### Generated Columns 自動計算
- `has_media`: 自動檢測題目是否包含媒體檔案
- `has_images`: 自動檢測是否包含圖片
- `has_audio`: 自動檢測是否包含音訊
- `has_video`: 自動檢測是否包含影片
- `option_count`: 自動計算選擇題選項數量

### 索引策略
- **單欄位索引**: 常用查詢欄位
- **複合索引**: 多條件查詢優化
- **全文索引**: 題目標題搜尋
- **外鍵索引**: 關聯查詢效能保證

### 視圖 (Views)
- `question_details`: 題目詳細資訊彙整
- `exam_overview`: 測驗概覽統計
- `user_exam_records`: 使用者測驗記錄

---

## 🛠️ 維護建議

### 定期維護
1. **清理過期會話**: 刪除超過 7 天的未完成會話
2. **更新統計資料**: 每日更新 exam_statistics 和 question_statistics
3. **媒體檔案清理**: 清理未使用的音訊/影片檔案
4. **索引優化**: 定期分析慢查詢並優化索引

### 備份策略
1. **每日增量備份**: 備份當日新增/修改資料
2. **每週完整備份**: 完整資料庫備份
3. **媒體檔案備份**: 定期備份 media 目錄

### 監控指標
- 資料庫連線數
- 慢查詢數量
- 儲存空間使用率
- 測驗完成率統計

---

## 📈 版本資訊

- **版本**: 1.0
- **建立日期**: 2025-05-23
- **資料庫版本**: MariaDB 11.3+
- **維護者**: 開發團隊
- **最後更新**: 2025-05-23

---

**注意**: 此文件會隨系統需求變更而更新，請定期檢查最新版本。