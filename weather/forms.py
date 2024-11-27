from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.mail import send_mail
import random
import string

# Form for sign up
class SignUpForm(forms.ModelForm):
    username= forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    otp = forms.CharField(max_length=6, required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Check if the email is already in use
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email is already in use.")
        return email

    # OTP generation method
    def generate_otp(self):
        otp = "".join(random.choices(string.digits, k=6))  # 6-digit OTP
        return otp

    # Method to send OTP to the email
    def send_otp_email(self, email, otp):
        subject = "Your OTP for Signup"
        message = f"Your OTP for signup is: {otp}"
        send_mail(subject, message, from_email="sharmaadarsh345678@gmail.com", recipient_list=[email])
