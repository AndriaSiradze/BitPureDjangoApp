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


class User(models.Model):
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    full_name = models.CharField(max_length=128)
    active = models.BooleanField()
    language = models.CharField(max_length=10)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'