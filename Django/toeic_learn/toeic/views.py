from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

import json
import requests # 確保 requests 函式庫已經安裝在你的虛擬環境中

# =====================================================================
# n8n Webhook URL 設定
# 請根據你 n8n 工作流程的 Webhook URL 進行修改
# 通常格式是 http://localhost:5678/webhook/你的Webhook_ID_或_Path
# 你的 Webhook ID 是 "django-test"
# =====================================================================
N8N_WEBHOOK_URL = "http://localhost:5678/webhook/django-test"

# 獲取當前使用的使用者模型 (Custom User Model or Django's default User)
User = get_user_model()

# =====================================================================
# 核心視圖函式
# =====================================================================

def home(request):
    """
    首頁視圖，顯示當前登入的使用者。
    """
    return render(request, 'home.html', {'user': request.user})

def user(request):
    """
    使用者頁面視圖。
    """
    return render(request, 'user.html')

def login_view(request):
    """
    登入頁面視圖，處理使用者登入。
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, '請輸入電子郵件和密碼')
            return render(request, 'login.html')

        try:
            # 嘗試根據 email 找到使用者
            # 注意：Django 預設的 User 模型是基於 username 認證
            # 如果你使用 email 登入，可能需要自定義 Authentication Backend 或確保 username 就是 email
            # 這裡假設你的 User 模型有 email 欄位，且你可以透過 email 找到使用者並用其 username 進行認證
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, '登入成功！')
                return redirect('home')
            else:
                messages.error(request, '帳號或密碼錯誤')
                return render(request, 'login.html')

        except User.DoesNotExist:
            messages.error(request, '該電子郵件未註冊')
            return render(request, 'login.html')

    return render(request, 'login.html')


# 由於你之前提供了 RegisterForm，但沒有提供其代碼
# 這裡我假設你已經在 forms.py 中定義了 RegisterForm
# 並且 RegisterForm 是用來創建新的 User 物件的
from .forms import RegisterForm # 確保你的 forms.py 存在這個表單

def register_view(request):
    """
    註冊頁面視圖，處理使用者註冊。
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save() # 保存新用戶
            messages.success(request, '註冊成功！')
            return redirect('home') # 通常註冊成功後會導向登入頁或首頁
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})

def test_page(request):
    """
    測試頁面視圖。
    """
    return render(request, 'test.html')

def ai_reading_test(request):
    """
    AI 閱讀測驗頁面視圖。
    """
    return render(request, 'ai_reading_test.html')

def reading_test(request):
    """
    閱讀測驗頁面視圖。
    """
    return render(request, 'reading_test.html')

def listening_test(request):
    """
    聽力測驗頁面視圖。
    """
    return render(request, 'listening_test.html')

@require_POST
@csrf_exempt
def vocab_test(request):
    """
    單字測驗視圖，向 n8n Webhook 發送請求並處理回應。
    """
    try:
        print("Attempting to connect to n8n...")
        response = requests.post(N8N_WEBHOOK_URL)
        response.raise_for_status() # 檢查 HTTP 請求是否成功

        print(f"n8n response status code: {response.status_code}")
        
        # 獲取原始的 JSON 字串
        raw_n8n_response_text = response.text
        print(f"Raw n8n response text: {raw_n8n_response_text}")

        # 解析 JSON
        n8n_response_data = response.json() 
        print(f"Parsed n8n response data (Python dict): {n8n_response_data}")
        
        questions_list = n8n_response_data.get('questions', []) 
        print(f"Extracted questions_list: {questions_list}")

        return render(request, 'vocab_test.html', {'questions': questions_list})

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to n8n: {e}")
        return JsonResponse({'error': f'Error connecting to n8n: {e}'}, status=500)
    except json.JSONDecodeError:
        # 如果 JSON 解析失敗，打印原始文本
        print(f"Failed to decode JSON from n8n response. Raw text: {response.text}")
        return JsonResponse({'error': 'Failed to decode JSON from n8n response. Check n8n response format.'}, status=500)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)


def record(request):
    """
    記錄頁面視圖。
    """
    return render(request, 'record.html')