-- --------------------------------------------------------
-- 主機:                           127.0.0.1
-- 伺服器版本:                        11.3.2-MariaDB - mariadb.org binary distribution
-- 伺服器作業系統:                      Win64
-- HeidiSQL 版本:                  12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- 傾印 114_system 的資料庫結構
CREATE DATABASE IF NOT EXISTS `114_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `114_system`;

-- 傾印  資料表 114_system.game_player 結構
CREATE TABLE IF NOT EXISTS `game_player` (
  `user_email` varchar(255) NOT NULL,
  `player_id` char(36) DEFAULT NULL,
  `game_session_id` char(36) DEFAULT NULL,
  `joined_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`user_email`),
  KEY `game_session_id` (`game_session_id`),
  CONSTRAINT `game_player_ibfk_1` FOREIGN KEY (`game_session_id`) REFERENCES `game_session` (`game_session_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.game_session 結構
CREATE TABLE IF NOT EXISTS `game_session` (
  `game_session_id` char(36) NOT NULL,
  `host_email` varchar(255) DEFAULT NULL,
  `game_type` varchar(255) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `is_private` tinyint(1) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `max_players` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `last_active_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`game_session_id`),
  KEY `host_email` (`host_email`),
  CONSTRAINT `game_session_ibfk_1` FOREIGN KEY (`host_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.point_transactions 結構
CREATE TABLE IF NOT EXISTS `point_transactions` (
  `id` char(36) NOT NULL,
  `user_email` varchar(255) DEFAULT NULL,
  `change_amount` int(11) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_email` (`user_email`),
  CONSTRAINT `point_transactions_ibfk_1` FOREIGN KEY (`user_email`) REFERENCES `users` (`email`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
-- 取消選取資料匯出。

-- 傾印  資料表 114_system.users 結構
CREATE TABLE IF NOT EXISTS `users` (
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nickname` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `point` int(11) DEFAULT 0,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- 取消選取資料匯出。

-- 英語學習考試系統資料庫設計
-- 支援 Reading、Vocab、Listen 三種考試模式及混合模式

-- 1. 考試主表
CREATE TABLE Exam (
    exam_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    exam_type ENUM('reading', 'vocab', 'listen', 'mixed') NOT NULL,
    duration_minutes INT DEFAULT 60,
    total_questions INT DEFAULT 0, -- 自動計算或手動設定
    passing_score DECIMAL(5,2) DEFAULT 60.00,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2. 文章表 (用於閱讀測驗)
CREATE TABLE Reading_Passage (
    passage_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL, -- 文章內容
    word_count INT DEFAULT 0, -- 字數統計
    reading_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'intermediate',
    topic VARCHAR(255), -- 文章主題，如 'science', 'history', 'literature'
    source VARCHAR(255), -- 文章來源
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 2.1 聽力材料表 (用於聽力測驗)
CREATE TABLE Listening_Material (
    material_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(500) NOT NULL,
    description TEXT, -- 聽力材料描述或摘要
    audio_url VARCHAR(500) NOT NULL, -- 音檔路徑
    transcript TEXT, -- 音檔文字稿 (可選)
    accent VARCHAR(100), -- 口音類型，如 'american', 'british', 'australian'
    topic VARCHAR(255), -- 聽力主題
    speaker_count INT DEFAULT 1, -- 說話人數量
    listening_level ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'intermediate',
    audio_quality ENUM('high', 'medium', 'low') DEFAULT 'high',
    source VARCHAR(255), -- 聽力材料來源
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. 題目表 (包含選項資訊)
CREATE TABLE Question (
    question_id INT PRIMARY KEY AUTO_INCREMENT,
    question_type ENUM('reading', 'vocab', 'listen') NOT NULL,
    passage_id INT NULL, -- 關聯到文章 (只有 reading 類型才會用到)
    material_id INT NULL, -- 關聯到聽力材料 (只有 listen 類型才會用到)
    question_text TEXT NOT NULL,
    question_image_url VARCHAR(500), -- 可選的圖片路徑
    
    -- Options
    option_a_text TEXT NOT NULL,
    option_b_text TEXT NOT NULL,
    option_c_text TEXT,
    option_d_text TEXT,
    option_e_text TEXT,
    
    -- Correct answers (支援單選和多選)
    -- 單選: "B", 多選: "AB", "ACD", "BCE" 等
    is_correct VARCHAR(10) NOT NULL, -- 儲存正確答案的組合，如 "A", "BC", "ABD"
    
    difficulty_level ENUM("1", "2", "3", "4", "5") DEFAULT "3",
    explanation TEXT, -- 題目解析
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (passage_id) REFERENCES Reading_Passage(passage_id) ON DELETE SET NULL,
    FOREIGN KEY (material_id) REFERENCES Listening_Material(material_id) ON DELETE SET NULL,
    INDEX idx_question_passage (passage_id),
    INDEX idx_question_material (material_id),
    INDEX idx_question_type (question_type)
);

-- 3. 考試題目關聯表
CREATE TABLE Exam_Question (
    exam_id INT NOT NULL,
    question_id INT NOT NULL,
    question_order INT NOT NULL, -- 題目在考試中的順序
    scores DECIMAL(5,2) DEFAULT 1.00, -- 該題在此考試中的分數
    PRIMARY KEY (exam_id, question_id),
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE,
    INDEX idx_exam_order (exam_id, question_order)
);

-- 4. 考試場次表
CREATE TABLE Exam_Session (
    session_id INT PRIMARY KEY AUTO_INCREMENT,
    exam_id INT NOT NULL,
    user_email VARCHAR(100) NOT NULL, -- 可以是學生ID或暫時識別碼
    time_limit_enabled BOOLEAN DEFAULT FALSE,
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    status ENUM('in_progress', 'completed', 'abandoned', 'timeout') DEFAULT 'in_progress',
    FOREIGN KEY (exam_id) REFERENCES Exam(exam_id) ON DELETE CASCADE,
    FOREIGN KEY (user_email) REFERENCES Users(user_email) ON DELETE CASCADE,
    INDEX idx_user_session (user_email, start_time),
    INDEX idx_exam_session (user_email, status)
);

-- 5. 使用者答案表
CREATE TABLE User_Answer (
    answer_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    question_id INT NOT NULL,
    selected_options VARCHAR(10) NOT NULL, -- 儲存使用者選擇，如 "B", "AC", "BDE"
    answer_text TEXT, -- 如果有填空題或簡答題
    is_correct BOOLEAN, -- 計算後的結果
    answer_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Exam_Session(session_id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES Question(question_id) ON DELETE CASCADE,
    UNIQUE KEY unique_session_question (session_id, question_id),
    INDEX idx_session_answer (session_id)
);

-- 6. 考試結果表
CREATE TABLE Exam_Result (
    result_id INT PRIMARY KEY AUTO_INCREMENT,
    session_id INT NOT NULL,
    total_questions INT NOT NULL,
    correct_answers INT DEFAULT 0,
    total_score DECIMAL(5,2) DEFAULT 0.00,
    is_passed BOOLEAN DEFAULT FALSE,
    reading_score DECIMAL(5,2) DEFAULT NULL, -- 分類成績
    vocab_score DECIMAL(5,2) DEFAULT NULL,
    listen_score DECIMAL(5,2) DEFAULT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES Exam_Session(session_id) ON DELETE CASCADE,
    UNIQUE KEY unique_session_result (session_id)
);
