from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from .forms import SignUpForm

def signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        auth_login(request, user) # 创建用户的同时使用该用户登陆
        return redirect('boards:home')
    else:
        return render(request, 'signup.html', {'form': form})
