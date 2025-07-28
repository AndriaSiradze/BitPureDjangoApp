import logging
from datetime import timedelta

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.generic import ListView, DetailView

from blogapp.forms import CommentForm
from blogapp.models import Title


# Create your views here.
def load_more_news(request):
    page_number = request.GET.get("page")
    news = Title.objects.exclude(translated_title__iexact='not related').prefetch_related('tags').order_by(
        '-created_at')
    paginator = Paginator(news, 21)
    try:
        page_obj = paginator.page(page_number)
    except Exception as err:
        logging.info(err)
        return HttpResponse("")  # если нет такой страницы, вернём пусто
    html = render_to_string("includes/_news_card_list.html", {"news_list": page_obj})
    return HttpResponse(html)


class TitleListView(ListView):
    model = Title
    template_name = "blogapp/titles_list.html"
    context_object_name = "news_list"
    paginate_by = 20

    def get_queryset(self):
        one_hour_ago = timezone.now() - timedelta(hours=1)
        qs = Title.objects.exclude(translated_title__iexact='not related')
        qs = qs.filter(created_at__lt=one_hour_ago)  # ← фильтр по времени
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
