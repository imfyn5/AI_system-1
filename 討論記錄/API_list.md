# 身分驗證相關
- /api/auth/login (POST) - 登入功能
- /api/auth/logout (POST) - 登出功能
- /api/auth/register (POST) - 註冊功能
- /api/auth/forgot-password (POST) - 忘記密碼功能，發送重設密碼郵件
- /api/auth/reset-password (POST) - 重設密碼功能，使用令牌重設密碼
- /api/auth/verify-email (GET/POST) - 驗證用戶電子郵件
- /api/auth/refresh-token (POST) - 刷新訪問令牌
- /api/auth/status (GET) - 檢查用戶的認證狀態
- /api/auth/google (GET/POST) - Google 第三方登入

# 題目相關
- /api/tests/{test_type}/questions (GET) - 獲取特定類型的題目列表
- /api/tests/{test_type}/questions/{question_id} (GET) - 獲取特定題目詳情
- /api/tests/{test_type}/questions/{question_id}/favorite (PUT) - 收藏/取消收藏題目
- /api/tests/{test_type}/favorites (GET) - 獲取特定類型的收藏題目
- /api/tests/{test_type}/wrong-questions (GET) - 獲取特定類型的錯題
- /api/tests/{test_type}/recommendations (GET) - 獲取特定類型的推薦題目

# 測驗相關
- /api/tests/{test_type}/exams (POST) - 創建/開始新測驗 (避免用"tests"造成混淆)
- /api/tests/{test_type}/exams/{exam_id} (GET) - 獲取測驗詳情
- /api/tests/{test_type}/exams/{exam_id}/submit (POST) - 提交測驗答案
- /api/tests/{test_type}/exams/{exam_id}/result (GET) - 獲取測驗結果
- /api/tests/{test_type}/history (GET) - 獲取特定類型的測驗歷史
- /api/tests/{test_type}/progress (GET) - 獲取特定類型的學習進度

# 跨類型的彙總數據
- /api/tests/history (GET) - 獲取所有測驗歷史記錄
- /api/tests/progress (GET) - 獲取所有類型的學習進度
- /api/tests/favorites (GET) - 獲取所有類型的收藏題目
- /api/tests/wrong-questions (GET) - 獲取所有類型的錯題

# 聽力測驗相關
- /api/listen/audio/{audio_id} (POST) - 獲取聽力音檔

# 發音測驗相關
- /api/speak/record (POST) - 上傳使用者的錄音檔案

# 網站內商店
- /api/shop/products (GET) - 獲取所有產品列表，支持分頁和過濾
- /api/shop/products/{product_id} (GET) - 獲取特定產品詳情
- /api/shop/products/search (GET) - 搜索產品
- /api/shop/categories (GET) - 獲取所有產品分類
- /api/shop/categories/{category_id}/products (GET) - 獲取特定分類下的產品

# 購物車相關
- /api/shop/cart (GET) - 獲取當前用戶的購物車
- /api/shop/cart/items (POST) - 添加商品到購物車
- /api/shop/cart/items/{item_id} (PUT) - 更新購物車中的商品數量
- /api/shop/cart/items/{item_id} (DELETE) - 從購物車中移除商品
- /api/shop/cart/clear (DELETE) - 清空購物車

# 訂單相關
- /api/shop/orders (GET) - 獲取用戶所有訂單
- /api/shop/orders (POST) - 創建新訂單
- /api/shop/orders/{order_id} (GET) - 獲取特定訂單詳情
- /api/shop/orders/{order_id}/cancel (POST) - 取消訂單
- /api/shop/orders/{order_id}/pay (POST) - 處理訂單支付

# 點數相關
- /api/shop/points (GET) - 獲取用戶點數餘額和基本狀態
- /api/shop/points/packages (GET) - 獲取可購買的點數套餐
- /api/shop/points/purchase (POST) - 購買點數
- /api/shop/points/transactions (GET) - 獲取點數交易記錄
- /api/shop/points/transactions/{transaction_id} (GET) - 獲取特定交易詳情

# 訂閱相關
- /api/shop/subscription-plans (GET) - 獲取可用的訂閱方案
- /api/shop/subscriptions (GET) - 獲取用戶當前訂閱狀態
- /api/shop/subscriptions (POST) - 創建新訂閱
- /api/shop/subscriptions/{subscription_id} (GET) - 獲取特定訂閱詳情
- /api/shop/subscriptions/{subscription_id}/cancel (POST) - 取消訂閱
- /api/shop/subscriptions/{subscription_id}/renew (POST) - 續期訂閱
- /api/shop/subscriptions/history (GET) - 獲取訂閱記錄

# 使用者相關
- /api/user/profile (GET) - 獲取用戶個人資料
- /api/user/profile (PUT) - 更新用戶個人資料
- /api/user/avatar (POST) - 上傳或更新用戶頭像
- /api/user/settings (GET) - 獲取用戶設置和偏好
- /api/user/settings (PUT) - 更新用戶設置和偏好
- /api/user/activity-log (GET) - 獲取帳號活動日誌

# 使用者學習資訊相關
- /api/user/tests (GET) - 獲取用戶的所有測驗記錄
- /api/user/tests/{test_type}/{test_id} (GET) - 獲取特定測驗的詳細結果
- /api/user/analysis (GET) - 獲取用戶的測驗分析和學習建議
- /api/user/performance (GET) - 獲取用戶表現的統計數據和趨勢

# 問題與反饋
- /api/user/issues (GET) - 獲取用戶提交的問題回報
- /api/user/issues (POST) - 提交新的問題回報
- /api/user/issues/{issue_id} (GET) - 獲取特定問題回報的詳情和狀態
- /api/user/feedback (POST) - 提交系統反饋或建議

# 遊戲相關
- /api/game

# AI 相關生成功能
- /api/ai/ 