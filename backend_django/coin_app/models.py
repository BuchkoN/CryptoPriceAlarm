from django.db import models

from bot_app.models import TelegramProfile


class Coin(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    price = models.DecimalField(max_digits=14, decimal_places=8, verbose_name='Стоимость')

    class Meta:
        verbose_name = 'Криптовалюта'
        verbose_name_plural = 'Криптовалюты'

    def __str__(self):
        return f'{self.name}'


class MonitoredCoin(models.Model):
    coin_id = models.ForeignKey(Coin, on_delete=models.CASCADE, verbose_name='ID криптовалюты')
    user_id = models.ForeignKey(TelegramProfile, on_delete=models.CASCADE, verbose_name='ID пользователя Telegram')
    expected_price = models.DecimalField(max_digits=14, decimal_places=8, verbose_name='Ожидаемая стоимость')

    class Meta:
        unique_together = ('user_id', 'coin_id')
        verbose_name = 'Отслеживаемая криптовалюта'
        verbose_name_plural = 'Отслеживаемые криптовалюты'

    def __str__(self):
        return f'{self.TelegramProfile.user_id} {self.Coin.name}'
