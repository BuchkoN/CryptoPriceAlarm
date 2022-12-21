from django.db import models


class TelegramProfile(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name='ID пользователя')
    username = models.CharField(max_length=25, verbose_name='Имя пользователя в Telegram', blank=True)

    class Meta:
        verbose_name = 'Профиль Telegram'
        verbose_name_plural = 'Профили Telegram'

    def __str__(self):
        return f'{self.username} ({self.user_id})'
