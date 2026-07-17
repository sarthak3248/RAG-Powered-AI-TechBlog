from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Contact


class RegisterForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment

        fields = ["content"]

        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Share your thoughts..."
                }
            )
        }

        labels = {
            "content": ""
        }
        
class ContactForm(forms.ModelForm):
    
    class Meta:
        
        model = Contact
        
        fields = [
            "name",
            "email",
            "subject",
            "message"
        ]        
        
        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Name"
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your Email"
                }
            ),

            "subject": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Subject"
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Write your message..."
                }
            )

        }