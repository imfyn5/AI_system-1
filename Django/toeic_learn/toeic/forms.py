from django import forms
from .models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True, label="確認密碼")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # 這裡不包括 confirm_password
    
    # 驗證密碼是否匹配
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("密碼和確認密碼不一致")
        return cleaned_data

