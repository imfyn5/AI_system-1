from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from toeic.models import ReadingPassage, Question
import json
from .models import ReadingPassage, Question,UserAnswer,ExamResult
from django.utils import timezone
from datetime import timedelta
from .models import Exam, ExamQuestion, ExamSession
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper

# 獲取當前使用的使用者模型
User = get_user_model()

# 首頁、使用者頁面、登入、註冊、測試頁面等不變
def home(request):
    return render(request, 'home.html', {'user': request.user})

def user(request):
    return render(request, 'user.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, '請輸入電子郵件和密碼')
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, '登入成功！')
            return redirect('home')
        else:
            messages.error(request, '帳號或密碼錯誤')
            return render(request, 'login.html')

    return render(request, 'login.html')

from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '註冊成功！請登入。')
            return redirect('login')
        else:
            messages.error(request, '註冊失敗，請檢查表單內容。')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def test_page(request):
    return render(request, 'test.html')

def generate_reading_view(request):
    return render(request, 'generate_form.html')

def ai_reading_test(request):
    return render(request, 'ai_reading_test.html')

def listening_test(request):
    return render(request, 'listening_test.html')

def record(request):
    return render(request, 'record.html')

def generated_reading_test_view(request):
    return render(request, 'generated_reading_test.html')


# ===== 以下為去除 n8n 呼叫的 API 及頁面 =====

from django.shortcuts import render
from toeic.models import Question
import random

def reading_test(request):
    # 隨機抽取一篇已審核的文章
    passages = ReadingPassage.objects.filter(is_approved=True)  # 假設有 is_approved 欄位標示審核狀態
    if not passages.exists():
        return render(request, 'reading_test.html', {'error': '目前沒有已審核的文章'})

    passage = random.choice(passages)

    # 取得該文章的所有題目
    questions = Question.objects.filter(passage=passage)

    # 將資料包成 dict 傳給模板
    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
        'source': passage.source,
    }

    # 將題目轉成 list of dict，方便 JS 使用
    questions_data = []
    for q in questions:
        questions_data.append({
            'question_id': q.question_id,
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'option_e_text': q.option_e_text,
            'difficulty_level': q.difficulty_level,
        })

    import json
    # 把題目序列化成JSON字串，安全傳到模板
    questions_json = json.dumps(questions_data)

    return render(request, 'reading_test.html', {
        'passage': passage_data,
        'questions_json': questions_json,
    })


@require_http_methods(["POST"])
def generate_reading_passage_api(request):
    """
    不再呼叫 n8n，直接模擬成功回應
    """
    try:
        data = json.loads(request.body)
        topic = data.get('topic')
        reading_level = data.get('reading_level')

        if not topic or not reading_level:
            return JsonResponse({'success': False, 'error': '請提供主題和閱讀級別'})

        # 模擬生成資料
        simulated_data = {
            'passage': {
                'title': f'{topic} 文章',
                'topic': topic,
                'word_count': 120,
                'reading_level': reading_level,
                'source': '模擬資料',
                'content': f'這是一篇關於 {topic} 的 {reading_level} 文章。'
            },
            'questions': []
        }

        return JsonResponse({'success': True, 'data': simulated_data})

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': '無效的 JSON 格式'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': f'服務器錯誤: {str(e)}'})

@csrf_exempt
@require_POST
def submit_test_answer(request):
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        answers = data.get('answers')  # dict: {question_id: selected_option}

        if not session_id or not answers:
            return JsonResponse({'success': False, 'error': '缺少 session_id 或 answers'})

        try:
            session = ExamSession.objects.get(session_id=session_id)
        except ExamSession.DoesNotExist:
            return JsonResponse({'success': False, 'error': '找不到考試紀錄'})

        # 防止重複提交
        if session.status == 'completed':
            return JsonResponse({'success': False, 'error': '本次測驗已完成，請勿重複提交'})

        correct_count = 0
        total_questions = len(answers)
        answer_time = timezone.now()
        question_details = []

        for qid, selected_option in answers.items():
            try:
                question = Question.objects.get(question_id=qid)
            except Question.DoesNotExist:
                continue

            is_correct = (selected_option.lower() == question.is_correct.lower())
            if is_correct:
                correct_count += 1

            # 儲存每一題作答
            UserAnswer.objects.create(
                session=session,
                question=question,
                selected_options=selected_option,
                is_correct=is_correct,
                answer_time=answer_time,
            )

            # 組詳解
            options = [
                {'value': 'a', 'text': question.option_a_text},
                {'value': 'b', 'text': question.option_b_text},
                {'value': 'c', 'text': question.option_c_text},
                {'value': 'd', 'text': question.option_d_text},
            ]
            if question.option_e_text:
                options.append({'value': 'e', 'text': question.option_e_text})

            question_details.append({
                'question_id': str(qid),
                'question_text': question.question_text,
                'user_answer': selected_option,
                'correct_answer': question.is_correct,
                'is_correct': is_correct,
                'explanation': question.explanation,
                'options': options,
            })

        # 計算分數
        score_percentage = round(correct_count / total_questions * 100, 2)
        is_passed = score_percentage >= float(session.exam.passing_score)

        # 儲存 ExamResult
        ExamResult.objects.create(
            session=session,
            total_questions=total_questions,
            correct_answers=correct_count,
            total_score=score_percentage,
            is_passed=is_passed,
            reading_score=score_percentage if session.exam.exam_type == 'reading' else 0,
            vocab_score=0,
            listen_score=score_percentage if session.exam.exam_type == 'listen' else 0,
            completed_at=timezone.now(),
        )

        # 更新 session 狀態
        session.status = 'completed'
        session.end_time = timezone.now()
        session.save()

        return JsonResponse({
            'success': True,
            'data': {
                'score': score_percentage,
                'correct_answers': correct_count,
                'total_questions': total_questions,
                'is_passed': is_passed,
                'question_details': question_details,
            }
        })

    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def test_result(request):
    """
    顯示測驗結果頁面，內容不變
    """
    context = {
        'page_title': '測驗結果',
        'test_type': 'reading'
    }
    return render(request, 'result.html', context)

def all_test_view(request):
    """
    顯示綜合測驗頁面
    """
    return render(request, 'all_test.html')

def part2(request):
    """
    處理「應答問題」頁面顯示。
    """
    return render(request, 'part2.html')

def part3(request):
    """
    處理「簡短對白」頁面顯示。
    """
    return render(request, 'part3.html') 

def part5(request):
    part_number = 5

    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part5.html', {'error': '目前沒有 Part 5 的考卷'})
    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    for eq in exam_questions:
        q = eq.question
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'option_e_text': q.option_e_text,
            'difficulty_level': q.difficulty_level,
        })

    import json
    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part5.html', context)

def part6(request):
    part_number = 6

    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part6.html', {'error': '目前沒有 Part 6 的考卷'})
    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    passage = None
    for eq in exam_questions:
        q = eq.question
        if not passage and q.passage:
            passage = q.passage
        questions_data.append({
            'question_id': str(q.question_id),  # <-- 轉字串
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'option_e_text': q.option_e_text,
            'difficulty_level': q.difficulty_level,
        })

    if not passage:
        return render(request, 'part6.html', {'error': '考卷中未找到對應文章'})

    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
        'source': passage.source,
    }

    import json
    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'passage': passage_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,
    }
    return render(request, 'part6.html', context)


@login_required
@require_POST
def submit_part6_answers(request):
    user = request.user
    exam_id = request.POST.get("exam_id")
    question_ids = request.POST.getlist("question_ids[]")

    for qid in question_ids:
        question = Question.objects.get(id=qid)
        selected_answer = request.POST.get(f"answer_{qid}")

        # 儲存使用者作答
        UserAnswer.objects.create(
            user=user,
            question=question,
            selected_answer=selected_answer,
            is_correct=(selected_answer == question.correct_answer),
        )

    messages.success(request, "作答完成，已儲存答案！")
    return redirect("quiz:part6_result")

def part7(request):
    part_number = 7

    # 取得所有有 Part 7 題目的考卷
    exam_ids = ExamQuestion.objects.filter(question__part=part_number).values_list('exam_id', flat=True).distinct()
    if not exam_ids:
        return render(request, 'part7.html', {'error': '目前沒有 Part 7 的考卷'})

    selected_exam_id = random.choice(list(exam_ids))
    exam = Exam.objects.get(pk=selected_exam_id)

    # 取出這份考卷的所有 Part 7 題目
    exam_questions = ExamQuestion.objects.filter(exam=exam, question__part=part_number).select_related('question').order_by('question_order')

    questions_data = []
    passage = None
    for eq in exam_questions:
        q = eq.question
        if not passage and q.passage:
            passage = q.passage
        questions_data.append({
            'question_id': str(q.question_id),
            'question_text': q.question_text,
            'option_a_text': q.option_a_text,
            'option_b_text': q.option_b_text,
            'option_c_text': q.option_c_text,
            'option_d_text': q.option_d_text,
            'option_e_text': q.option_e_text,
            'difficulty_level': q.difficulty_level,
        })

    if not passage:
        return render(request, 'part7.html', {'error': '考卷中未找到對應文章'})

    passage_data = {
        'title': passage.title,
        'content': passage.content,
        'topic': passage.topic,
        'word_count': passage.word_count,
        'reading_level': passage.reading_level,
        'source': passage.source,
    }

    questions_json = json.dumps(questions_data)

    user = request.user
    if not user.is_authenticated:
        return redirect('login')

    session = ExamSession.objects.create(
        exam=exam,
        user=user,
        time_limit_enabled=False,
        start_time=timezone.now(),
        end_time=timezone.now(),
        status='in_progress',
    )

    context = {
        'passage': passage_data,
        'questions_json': questions_json,
        'exam_id': exam.exam_id,
        'session_id': session.session_id,  # <--- 傳給前端
    }
    return render(request, 'part7.html', context)


def exam_part_view(request, part_number):
    # 取得包含該 part 的所有考卷 ID（exam_id 是你的主鍵名稱）
    exam_ids_with_part = ExamQuestion.objects.filter(
        question__part=part_number
    ).values_list('exam_id', flat=True).distinct()

    if not exam_ids_with_part:
        return render(request, 'no_exam_found.html', {'part': part_number})

    selected_exam_id = random.choice(list(exam_ids_with_part))
    selected_exam = Exam.objects.get(exam_id=selected_exam_id)

    part_questions = ExamQuestion.objects.filter(
        exam=selected_exam, question__part=part_number
    ).select_related('question').order_by('question_order')

    # 對應每個 part 要使用的模板
    template_map = {
        2: 'part2.html',
        3: 'part3.html',
        5: 'part5.html',
        6: 'part6.html',
        7: 'part7.html',
    }
    template_name = template_map.get(part_number, 'default_exam_part.html')

    context = {
        'exam': selected_exam,
        'questions': [eq.question for eq in part_questions],
        'part': part_number,
    }
    return render(request, template_name, context)


@csrf_exempt
def update_exam_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        session_id = data.get('session_id')
        new_status = data.get('status')

        try:
            session = ExamSession.objects.get(session_id=session_id)

            # 根據狀態更新欄位
            if new_status == 'in_progress':
                session.status = 'in_progress'
                session.start_time = timezone.now()
            elif new_status == 'completed':
                session.status = 'completed'
                session.end_time = timezone.now()

            session.save()
            return JsonResponse({'success': True})
        except ExamSession.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Session not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request'})    

@login_required
def record(request):
    user = request.user

    # 歷史測驗紀錄
    exam_results = (
        ExamResult.objects
        .filter(session__user=user)
        .order_by('-completed_at')
        .select_related('session__exam')
    )

    # 閱讀/聽力進度
    reading_total = UserAnswer.objects.filter(session__user=user, question__question_type='reading').count()
    reading_correct = UserAnswer.objects.filter(session__user=user, question__question_type='reading', is_correct=True).count()
    listening_total = UserAnswer.objects.filter(session__user=user, question__question_type='listen').count()
    listening_correct = UserAnswer.objects.filter(session__user=user, question__question_type='listen', is_correct=True).count()

    reading_progress = int((reading_correct / reading_total) * 100) if reading_total else 0
    listening_progress = int((listening_correct / listening_total) * 100) if listening_total else 0

    # 總學習時數
    total_answers = UserAnswer.objects.filter(session__user=user).count()
    study_hours = round(total_answers / 60, 1)  # 1題1分鐘，60題=1小時

    context = {
        'user': user,
        'exam_results': exam_results,
        'reading_progress': reading_progress,
        'listening_progress': listening_progress,
        'study_hours': study_hours,
    }
    return render(request, 'record.html', context)