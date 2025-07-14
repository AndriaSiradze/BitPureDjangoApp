from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView

from blogapp.forms import CommentForm
from blogapp.models import Title


# Create your views here.

class TitleListView(ListView):
    model = Title
    template_name = "blogapp/titles_list.html"
    context_object_name = "news_list"
    paginate_by = 6

    def get_queryset(self):
        qs = Title.objects.exclude(translated_title__iexact='None')
        qs = qs.prefetch_related('tags')
        return qs.order_by('-created_at')


class TitleDetailView(DetailView):
    model = Title
    template_name = 'blogapp/title_detail.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.article = self.object
            comment.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Catching
                return render(
                    request,
                    'includes/_comment.html',
                    {'comment': comment},
                    status=201
                )
        return redirect('blogapp:title_detail', pk=self.object.pk)
