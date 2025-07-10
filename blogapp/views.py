from django.views.generic import TemplateView, ListView, DetailView

from blogapp.models import Title


# Create your views here.

class TitleListView(ListView):
    model = Title
    template_name = "blogapp/titles_list.html"
    context_object_name = "news_list"
    paginate_by = 8

    def get_queryset(self):
        qs = Title.objects.exclude(translated_title__iexact='None')
        qs = qs.prefetch_related('tags')
        return qs.order_by('-created_at')


class TitleDetailView(DetailView):
    model = Title
    template_name = 'blogapp/title_detail.html'
    context_object_name = 'article'

