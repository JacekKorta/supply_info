
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView

from info_channel.models import Post


@method_decorator(login_required, name='dispatch')
class PostListView(ListView):

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.published.prefetch_related('post_body_paragraph').all()
        else:
            return Post.published.prefetch_related('post_body_paragraph').exclude(category='inner_information')

    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'info_channel/post/list.html'


@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    model = Post
    template_name = 'info_channel/post/detail.html'
