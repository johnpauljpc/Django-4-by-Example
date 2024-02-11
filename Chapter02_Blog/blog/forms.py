from django import forms
from . import models

class EmailPostForm(forms.Form):
    sender_name = forms.CharField()
    sender_email = forms.EmailField()
    reciever_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)

 

class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['name', 'email','content']