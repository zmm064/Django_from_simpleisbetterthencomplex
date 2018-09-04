from django import forms
from .models import Topic, Post

class NewTopicForm(forms.ModelForm):
    # 定义一个额外的字段
    message = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder':'请输入内容...'}), 
        label='内容',
        error_messages = {'required': '话题内容不能为空'}
    )

    class Meta:
        model = Topic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message', ]