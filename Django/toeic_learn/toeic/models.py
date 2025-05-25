from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    email = models.EmailField(unique=True)
    point = models.IntegerField(default=0)

    # 避免與 Django 預設的 User 模型衝突
    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    def __str__(self):
        return self.email

class Question(models.Model):
    QUESTION_TYPE_CHOICES = [
        ('vocab', 'Vocabulary'),
        ('reading', 'Reading'),
        ('listen', 'Listening'),
    ]

    question_type = models.CharField(max_length=20, choices=QUESTION_TYPE_CHOICES, default='vocab')
    question_text = models.TextField()
    option_a_text = models.TextField()
    option_b_text = models.TextField()
    option_c_text = models.TextField()
    option_d_text = models.TextField()
    is_correct = models.CharField(max_length=1)  # 存 'a'、'b'、'c'、'd'
    difficulty_level = models.IntegerField(default=1)
    explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)