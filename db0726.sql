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
CREATE DATABASE IF NOT EXISTS `114_system` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `114_system`;

-- 傾印  資料表 114_system.auth_group 結構
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.auth_group_permissions 結構
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.auth_permission 結構
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.django_admin_log 結構
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_toeic_user_email` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_toeic_user_email` FOREIGN KEY (`user_id`) REFERENCES `toeic_user` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.django_content_type 結構
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.django_migrations 結構
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.django_session 結構
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_exam 結構
CREATE TABLE IF NOT EXISTS `toeic_exam` (
  `exam_id` uuid NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `exam_type` varchar(20) NOT NULL,
  `part` int(11) DEFAULT NULL,
  `duration_minutes` int(11) NOT NULL,
  `total_questions` int(11) NOT NULL,
  `passing_score` decimal(5,2) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`exam_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_examquestion 結構
CREATE TABLE IF NOT EXISTS `toeic_examquestion` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `question_order` int(11) NOT NULL,
  `scores` decimal(5,2) NOT NULL,
  `exam_id` uuid NOT NULL,
  `question_id` uuid NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `toeic_examquestion_exam_id_question_id_e98f0892_uniq` (`exam_id`,`question_id`),
  KEY `toeic_examquestion_question_id_ba904ce7_fk_toeic_que` (`question_id`),
  CONSTRAINT `toeic_examquestion_exam_id_a8eea86c_fk_toeic_exam_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `toeic_exam` (`exam_id`),
  CONSTRAINT `toeic_examquestion_question_id_ba904ce7_fk_toeic_que` FOREIGN KEY (`question_id`) REFERENCES `toeic_question` (`question_id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_examresult 結構
CREATE TABLE IF NOT EXISTS `toeic_examresult` (
  `result_id` uuid NOT NULL,
  `total_questions` int(11) NOT NULL,
  `correct_answers` int(11) NOT NULL,
  `total_score` decimal(5,2) NOT NULL,
  `is_passed` tinyint(1) NOT NULL,
  `reading_score` decimal(5,2) NOT NULL,
  `vocab_score` decimal(5,2) NOT NULL,
  `listen_score` decimal(5,2) NOT NULL,
  `completed_at` datetime(6) NOT NULL,
  `session_id` uuid NOT NULL,
  PRIMARY KEY (`result_id`),
  UNIQUE KEY `session_id` (`session_id`),
  CONSTRAINT `toeic_examresult_session_id_149ed859_fk_toeic_exa` FOREIGN KEY (`session_id`) REFERENCES `toeic_examsession` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_examsession 結構
CREATE TABLE IF NOT EXISTS `toeic_examsession` (
  `session_id` uuid NOT NULL,
  `time_limit_enabled` tinyint(1) NOT NULL,
  `start_time` datetime(6) NOT NULL,
  `end_time` datetime(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `exam_id` uuid NOT NULL,
  `user_id` varchar(254) NOT NULL,
  PRIMARY KEY (`session_id`),
  KEY `toeic_examsession_exam_id_33883b47_fk_toeic_exam_exam_id` (`exam_id`),
  KEY `toeic_examsession_user_id_fd22957f_fk_toeic_user_email` (`user_id`),
  CONSTRAINT `toeic_examsession_exam_id_33883b47_fk_toeic_exam_exam_id` FOREIGN KEY (`exam_id`) REFERENCES `toeic_exam` (`exam_id`),
  CONSTRAINT `toeic_examsession_user_id_fd22957f_fk_toeic_user_email` FOREIGN KEY (`user_id`) REFERENCES `toeic_user` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_listeningmaterial 結構
CREATE TABLE IF NOT EXISTS `toeic_listeningmaterial` (
  `material_id` uuid NOT NULL,
  `audio_url` varchar(255) DEFAULT NULL,
  `transcript` longtext NOT NULL,
  `accent` varchar(50) DEFAULT NULL,
  `topic` varchar(255) NOT NULL,
  `listening_level` varchar(20) NOT NULL,
  `source` varchar(255) DEFAULT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `rejection_reason` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`material_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_pointtransaction 結構
CREATE TABLE IF NOT EXISTS `toeic_pointtransaction` (
  `id` uuid NOT NULL,
  `change_amount` int(11) NOT NULL,
  `reason` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` varchar(254) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `toeic_pointtransaction_user_id_2fa8a923_fk_toeic_user_email` (`user_id`),
  CONSTRAINT `toeic_pointtransaction_user_id_2fa8a923_fk_toeic_user_email` FOREIGN KEY (`user_id`) REFERENCES `toeic_user` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_question 結構
CREATE TABLE IF NOT EXISTS `toeic_question` (
  `question_id` uuid NOT NULL,
  `question_type` varchar(20) NOT NULL,
  `part` int(11) DEFAULT NULL,
  `question_text` longtext NOT NULL,
  `option_a_text` longtext NOT NULL,
  `option_b_text` longtext NOT NULL,
  `option_c_text` longtext NOT NULL,
  `option_d_text` longtext NOT NULL,
  `option_e_text` longtext DEFAULT NULL,
  `is_correct` varchar(1) NOT NULL,
  `difficulty_level` int(11) NOT NULL,
  `explanation` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `question_category` varchar(10) NOT NULL,
  `material_id` uuid DEFAULT NULL,
  `passage_id` uuid DEFAULT NULL,
  PRIMARY KEY (`question_id`),
  KEY `toeic_question_material_id_c34c9a86_fk_toeic_lis` (`material_id`),
  KEY `toeic_question_passage_id_23a9ed6a_fk_toeic_rea` (`passage_id`),
  CONSTRAINT `toeic_question_material_id_c34c9a86_fk_toeic_lis` FOREIGN KEY (`material_id`) REFERENCES `toeic_listeningmaterial` (`material_id`),
  CONSTRAINT `toeic_question_passage_id_23a9ed6a_fk_toeic_rea` FOREIGN KEY (`passage_id`) REFERENCES `toeic_readingpassage` (`passage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_readingpassage 結構
CREATE TABLE IF NOT EXISTS `toeic_readingpassage` (
  `passage_id` uuid NOT NULL,
  `title` varchar(255) NOT NULL,
  `content` longtext NOT NULL,
  `word_count` int(11) NOT NULL,
  `reading_level` varchar(20) NOT NULL,
  `topic` varchar(255) NOT NULL,
  `source` varchar(255) NOT NULL,
  `is_approved` tinyint(1) NOT NULL,
  `rejection_reason` varchar(50) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`passage_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_user 結構
CREATE TABLE IF NOT EXISTS `toeic_user` (
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `email` varchar(254) NOT NULL,
  `nickname` varchar(50) NOT NULL,
  `point` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_useranswer 結構
CREATE TABLE IF NOT EXISTS `toeic_useranswer` (
  `answer_id` uuid NOT NULL,
  `selected_options` varchar(10) NOT NULL,
  `answer_text` longtext DEFAULT NULL,
  `is_correct` tinyint(1) NOT NULL,
  `answer_time` datetime(6) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `question_id` uuid NOT NULL,
  `session_id` uuid NOT NULL,
  PRIMARY KEY (`answer_id`),
  KEY `toeic_useranswer_question_id_2442d5e4_fk_toeic_que` (`question_id`),
  KEY `toeic_useranswer_session_id_9fb4780d_fk_toeic_exa` (`session_id`),
  CONSTRAINT `toeic_useranswer_question_id_2442d5e4_fk_toeic_que` FOREIGN KEY (`question_id`) REFERENCES `toeic_question` (`question_id`),
  CONSTRAINT `toeic_useranswer_session_id_9fb4780d_fk_toeic_exa` FOREIGN KEY (`session_id`) REFERENCES `toeic_examsession` (`session_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_user_groups 結構
CREATE TABLE IF NOT EXISTS `toeic_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(254) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `toeic_user_groups_user_id_group_id_2a14fa8a_uniq` (`user_id`,`group_id`),
  KEY `toeic_user_groups_group_id_ca2fc59e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `toeic_user_groups_group_id_ca2fc59e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `toeic_user_groups_user_id_7ef3a7ad_fk_toeic_user_email` FOREIGN KEY (`user_id`) REFERENCES `toeic_user` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

-- 傾印  資料表 114_system.toeic_user_user_permissions 結構
CREATE TABLE IF NOT EXISTS `toeic_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` varchar(254) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `toeic_user_user_permissions_user_id_permission_id_7d8c73e9_uniq` (`user_id`,`permission_id`),
  KEY `toeic_user_user_perm_permission_id_f59d8de2_fk_auth_perm` (`permission_id`),
  CONSTRAINT `toeic_user_user_perm_permission_id_f59d8de2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `toeic_user_user_permissions_user_id_6abe38dc_fk_toeic_user_email` FOREIGN KEY (`user_id`) REFERENCES `toeic_user` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 取消選取資料匯出。

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
