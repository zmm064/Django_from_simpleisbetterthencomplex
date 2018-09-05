from django.http import HttpResponse
from boards.forms import PostForm
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator




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
            post.save() # 获得 post id
            # 更新topic
            topic.last_updated = timezone.now()
            topic.save()
            # 指定页面跳转的位置
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=reverse('boards:topic_posts', args=[pk, topic_pk]),
                id=post.pk,
                page=topic.get_page_count()
            )
            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})


class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message', )
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('boards:topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


class TopicListView(ListView):
    model = Topic
    context_object_name = 'topics'
    template_name = 'topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['board'] = self.board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
        queryset = self.board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
        return queryset


class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 2

    def get_context_data(self, **kwargs):
        sesseion_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(sesseion_key, False):
            # 使用session做条件判断
            self.topic.views += 1
            self.topic.save()
            self.request.session[sesseion_key] = True
        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(Topic, board__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('created_at')
        return queryset

