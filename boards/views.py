from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Board, User, Topic, Post
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)

    #if request.method == 'POST':
    #    subject = request.POST['subject']
    #    message = request.POST['message']

    #    user = User.objects.first()  # TODO: 临时使用一个账号作为登录用户
    #    topic = Topic.objects.create( subject=subject, board=board, starter=user )
    #    post = Post.objects.create( message=message, topic=topic, created_by=user )

    #    return redirect('boards:topics', pk=board.pk)  # TODO: redirect to the created topic page

    #return render(request, 'new_topic.html', {'board': board})
    form = NewTopicForm(request.POST or None)
    user = User.objects.first()
    if form.is_valid():
        topic = form.save(commit=False)
        topic.board = board
        topic.starter = user
        topic.save()
        post = Post.objects.create(
            message=form.cleaned_data.get('message'), 
            topic=topic, 
            created_by=user
        )
        return redirect('boards:topics', pk=board.pk)
    return render(request, 'new_topic.html', {'board': board, 'form': form})