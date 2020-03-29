from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from info_channel.models import Post


@method_decorator(login_required, name='dispatch')
class PostListView(ListView):
    model = Post.published

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category == 'all':
            if self.request.user.is_staff:
                return Post.published.prefetch_related('post_body_paragraph').all()
            else:
                return Post.published.prefetch_related('post_body_paragraph').exclude(category='inner_information')
        else:
            if self.request.user.is_staff:
                return Post.published.prefetch_related('post_body_paragraph').filter(category=category)
            else:
                return Post.published.prefetch_related('post_body_paragraph')\
                    .exclude(category='inner_information')\
                    .filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs.get('category')
        return context

    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'info_channel/post/list.html'


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'info_channel/post/detail.html'
