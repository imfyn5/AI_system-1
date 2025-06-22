from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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

def generate_reading_view(request):
    """
    顯示文章生成頁面
    """
    return render(request, 'generate_reading.html')

def ai_reading_test(request):
    """
    AI 閱讀測驗頁面視圖。
    """
    return render(request, 'ai_reading_test.html')

def reading_test(request):
    try:
        # 修正變數名稱衝突
        api_response = requests.get('http://n8n.ntub.local/webhook/tests/reading/question')
        
        # 檢查 API response status
        if api_response.status_code == 200:
            questions_data = api_response.json()
            print(f"API Response: {questions_data}")
            
            # 將資料傳遞給 template
            context = {
                'questions_data': questions_data
            }
            return render(request, 'reading_test.html', context)
        else:
            return JsonResponse({
                'error': f'API request failed with status: {api_response.status_code}'
            }, status=500)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'error': f'Failed to fetch questions: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'An unexpected error occurred: {str(e)}'
        }, status=500)

def listening_test(request):
    """
    聽力測驗頁面視圖。
    """
    return render(request, 'listening_test.html')

def vocab_test(request):
    try:
        # 修正變數名稱衝突
        api_response = requests.get('http://n8n.ntub.local/webhook/tests/vocab/question')
        
        # 檢查 API response status
        if api_response.status_code == 200:
            questions_data = api_response.json()
            print(f"API Response: {questions_data}")
            
            # 將資料傳遞給 template
            context = {
                'questions_data': questions_data
            }
            return render(request, 'vocab_test.html', context)
        else:
            return JsonResponse({
                'error': f'API request failed with status: {api_response.status_code}'
            }, status=500)
            
    except requests.exceptions.RequestException as e:
        return JsonResponse({
            'error': f'Failed to fetch questions: {str(e)}'
        }, status=500)
    except Exception as e:
        return JsonResponse({
            'error': f'An unexpected error occurred: {str(e)}'
        }, status=500)

def record(request):
    """
    記錄頁面視圖。
    """
    return render(request, 'record.html')

def generate_reading_view(request):
    """
    顯示文章生成表單頁面
    """
    return render(request, 'generate_form.html')

def generated_reading_test_view(request):
    """
    顯示生成的閱讀測驗頁面
    """
    return render(request, 'generated_reading_test.html')

@require_http_methods(["POST"])
def generate_reading_passage_api(request):
    """
    Django 作為代理，轉發請求到 n8n webhook
    """
    try:
        # 解析前端請求
        data = json.loads(request.body)
        topic = data.get('topic')
        reading_level = data.get('reading_level')
        
        # 驗證輸入
        if not topic or not reading_level:
            return JsonResponse({
                'success': False,
                'error': '請提供主題和閱讀級別'
            })
        
        # 驗證有效選項
        valid_topics = ['science', 'entertainment']
        valid_levels = ['beginner', 'intermediate', 'advanced']
        
        if topic not in valid_topics:
            return JsonResponse({
                'success': False,
                'error': '無效的主題選擇'
            })
            
        if reading_level not in valid_levels:
            return JsonResponse({
                'success': False,
                'error': '無效的閱讀級別選擇'
            })
        
        # 轉發請求到 n8n webhook
        n8n_url = 'http://n8n.ntub.local/webhook/tests/ai_reading/question'
        
        try:
            # 發送請求到 n8n
            response = requests.post(
                n8n_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=120  # 設定較長的超時時間，因為 AI 生成需要時間
            )
            
            # 檢查 n8n 回應
            if response.status_code == 200:
                n8n_data = response.json()
                return JsonResponse({
                    'success': True,
                    'data': n8n_data
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'n8n webhook 錯誤: {response.status_code}'
                })
                
        except requests.Timeout:
            return JsonResponse({
                'success': False,
                'error': 'AI 生成超時，請稍後再試'
            })
        except requests.RequestException as e:
            return JsonResponse({
                'success': False,
                'error': f'連線到 AI 服務失敗: {str(e)}'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '無效的 JSON 格式'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'服務器錯誤: {str(e)}'
        })
    
@require_http_methods(["POST"])
def submit_test_answer(request):
    """
    Django 作為 proxy，轉發答案提交請求到 n8n webhook
    """
    try:
        # 解析前端請求
        data = json.loads(request.body)
        
        # 驗證必要欄位
        required_fields = ['answers', 'test_type', 'total_questions']
        for field in required_fields:
            if field not in data:
                return JsonResponse({
                    'success': False,
                    'error': f'缺少必要欄位: {field}'
                })
        
        answers = data.get('answers')
        test_type = data.get('test_type')
        total_questions = data.get('total_questions')
        
        # 驗證答案格式
        if not isinstance(answers, dict):
            return JsonResponse({
                'success': False,
                'error': '答案格式錯誤，應為物件格式'
            })
        
        # 驗證題目數量
        if not isinstance(total_questions, int) or total_questions <= 0:
            return JsonResponse({
                'success': False,
                'error': '題目數量必須為正整數'
            })
        
        # 驗證答案選項格式 (假設為 a, b, c, d)
        valid_options = ['a', 'b', 'c', 'd']
        for question_id, answer in answers.items():
            if answer not in valid_options:
                return JsonResponse({
                    'success': False,
                    'error': f'題目 {question_id} 的答案選項無效: {answer}'
                })
        
        # 轉發請求到 n8n webhook
        n8n_url = 'http://n8n.ntub.local/webhook/api/test/answer'
        
        try:
            # 發送請求到 n8n (保持原始資料格式)
            response = requests.post(
                n8n_url,
                json=data,  # 直接轉發原始資料
                headers={'Content-Type': 'application/json'},
                timeout=60  # 答案提交通常不需要太長時間
            )
            
            # 檢查 n8n 回應
            if response.status_code == 200:
                n8n_data = response.json()
                return JsonResponse({
                    'success': True,
                    'data': n8n_data
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'n8n webhook 錯誤: {response.status_code}',
                    'details': response.text if response.text else None
                })
                
        except requests.Timeout:
            return JsonResponse({
                'success': False,
                'error': '答案提交超時，請稍後再試'
            })
        except requests.RequestException as e:
            return JsonResponse({
                'success': False,
                'error': f'連線到評分服務失敗: {str(e)}'
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': '無效的 JSON 格式'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'服務器錯誤: {str(e)}'
        })
    
def test_result(request):
    """
    顯示測驗結果頁面
    從 n8n 回傳的資料中渲染結果
    """
    # 可以從 session 或 GET 參數中獲取結果資料
    # 這裡提供基本的模板渲染，實際資料由前端 JavaScript 處理
    
    context = {
        'page_title': '測驗結果',
        'test_type': 'reading'  # 可以根據需要動態設定
    }
    
    return render(request, 'result.html', context)