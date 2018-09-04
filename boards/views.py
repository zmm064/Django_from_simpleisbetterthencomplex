from django.http import HttpResponse
from boards.forms import PostForm
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from .models import Board, User, Topic, Post
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

@login_required
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
        return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})