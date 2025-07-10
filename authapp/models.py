from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group, Permission, AbstractUser
from django.db import models


# Create your models here.


class TelegramBotUser(models.Model):
    """
    Representation of User Table From Telegram
    """
    user_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(max_length=128, blank=True, null=True)
    full_name = models.CharField(max_length=128)
    active = models.BooleanField()
    language = models.CharField(max_length=10)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'



class User(AbstractUser):
    telegram = models.OneToOneField(
        TelegramBotUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='django_user',
    )
    email = models.EmailField(unique=False, blank=True, verbose_name='email')

    def clean(self):
        super().clean()
        if self.email:
            self.email = self.email.lower()
