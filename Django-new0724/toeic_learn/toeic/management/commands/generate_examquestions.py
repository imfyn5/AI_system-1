from django.core.management.base import BaseCommand
from toeic.models import Exam, ExamQuestion, ReadingPassage, Question

class Command(BaseCommand):
    help = 'Generate Exam and ExamQuestions for all passages or parts, all questions included.'

    def handle(self, *args, **options):
        self.stdout.write("開始建立 Exam 與 ExamQuestion ...")

        # 處理有文章的 part
        passages = ReadingPassage.objects.all()
        for passage in passages:
            part = getattr(passage, 'part', None)
            if part is None:
                first_question = passage.question_set.first()
                if first_question:
                    part = getattr(first_question, 'part', None)
            if part is None:
                self.stdout.write(f"跳過文章 {passage.title}，無法取得 part")
                continue

            exam_title = f"Exam for Part {part} - {passage.title}"
            exam, created = Exam.objects.get_or_create(
                title=exam_title,
                defaults={
                    'description': "自動建立的測驗",
                    'exam_type': 'toeic',
                    'part': part,
                    'duration_minutes': 60,
                    'total_questions': passage.question_set.count(),
                    'passing_score': 70.0,
                    'is_active': True,
                }
            )
            if not created:
                self.stdout.write(f"{exam_title} 已存在，跳過建立")
                continue

            questions = passage.question_set.all().order_by('created_at')
            for idx, question in enumerate(questions, start=1):
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    question_order=idx,
                    scores=1.0,
                )
            self.stdout.write(f"建立 {exam_title}，共 {questions.count()} 題成功")

        # 處理無文章的 part，例如 Part 5
        parts_without_passage = [5]
        for part in parts_without_passage:
            questions = Question.objects.filter(part=part).order_by('created_at')
            if not questions.exists():
                self.stdout.write(f"Part {part} 沒有題目，跳過")
                continue

            exam_title = f"Exam for Part {part}"
            exam, created = Exam.objects.get_or_create(
                title=exam_title,
                defaults={
                    'description': "自動建立的測驗 (無文章)",
                    'exam_type': 'toeic',
                    'part': part,
                    'duration_minutes': 20,
                    'total_questions': questions.count(),
                    'passing_score': 60.0,
                    'is_active': True,
                }
            )
            if not created:
                self.stdout.write(f"{exam_title} 已存在，跳過建立")
                continue

            for idx, question in enumerate(questions, start=1):
                ExamQuestion.objects.create(
                    exam=exam,
                    question=question,
                    question_order=idx,
                    scores=1.0,
                )
            self.stdout.write(f"建立 {exam_title}，共 {questions.count()} 題成功")

        self.stdout.write("全部完成！")
