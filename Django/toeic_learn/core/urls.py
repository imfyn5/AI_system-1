"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from toeic import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", views.login_view, name="login"),
    path("register/",views.register_view, name="register"),
    path("", views.home, name="home"),
    path('test/', views.test_page, name='test'),
    path('ai_reading_test', views.ai_reading_test, name='ai_reading_test'),
    path('reading_test', views.reading_test, name='reading_test'),
    path('listening_test', views.listening_test, name='listening_test'),
    path('vocab_test', views.vocab_test, name='vocab_test'),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path('record/', views.record, name='record'),
    path('generate-reading/', views.generate_reading_view, name='generate_reading'),
    path('generated-reading-test/', views.generated_reading_test_view, name='generated_reading_test'),
    path('api/generate-reading-passage/', views.generate_reading_passage_api, name='generate_reading_passage_api'),
    path('api/submit_test_answer', views.submit_test_answer, name='submit_test_answer'),
    path('result/', views.test_result, name='test_result'),
]


