from django import forms
from django.forms import ModelForm
from .models import Book
from .models import Comment
from .models import Rating
from .models import ChatMessage

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = [
            'name',
            'web',
            'price',
            'picture',
        ]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...', 'rows': '3'})
        }


class RatingForm(ModelForm):
    class Meta:
        model = Rating
        fields = [
            'rating'
        ]


class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = [
            'text'
        ]
        labels = {
            'text': '',
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Your message', 'rows': '2'})
        }
