from django.conf import settings
from django.db import models
from django.urls import reverse


class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    name   = models.CharField(max_length=100)
    title  = models.ForeignKey(
        'Title',
        models.CASCADE,
        db_column='title_id',
        related_name='tags'
    )

    class Meta:
        managed = False
        db_table = 'tags'


class Title(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=500)
    source = models.CharField(max_length=500)
    created_at = models.DateTimeField()
    translated_title = models.CharField(max_length=500)
    original_text = models.TextField()
    preview = models.CharField(max_length=500)
    translated_post = models.TextField()

    class Meta:
        managed = False
        db_table = 'titles'

    def get_absolute_url(self):
        return reverse('blogapp:title_detail', kwargs={'pk': self.title_id})

class Url(models.Model):
    url_id = models.AutoField(primary_key=True)
    url = models.CharField(max_length=500)
    check_news = models.BooleanField()
    created_at = models.DateTimeField()
    type_of_feed = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'urls'


class Comment(models.Model):
    article = models.ForeignKey('Title', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='comment text')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"comment #{self.pk} for title {self.article}"




