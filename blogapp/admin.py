from django.contrib import admin

from blogapp.models import Title, Url


# Register your models here.
@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('title', 'translated_title', 'created_at',)  # какие поля показывать в списке
    search_fields = ('title', 'translated_title', 'tags__name')  # по каким искать
    list_filter = ('created_at',)  # фильтр справа


admin.site.register(Url)
