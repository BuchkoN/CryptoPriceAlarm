from django.contrib import admin

from coin_app.models import MonitoredCoin, Coin

admin.site.register(Coin)
admin.site.register(MonitoredCoin)
