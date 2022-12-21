from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework.viewsets import ModelViewSet

from coin_app.models import Coin, MonitoredCoin


class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        fields = ['id', 'name', 'price']


class MonitoredCoinSerializer(ModelSerializer):
    coin_name = CharField(read_only=True, source='coin_id.name')
    coin_price = CharField(read_only=True, source='coin_id.price')
    telegram_profile = CharField(read_only=True, source='user_id.user_id')

    class Meta:
        model = MonitoredCoin
        fields = ['id', 'user_id', 'coin_id', 'expected_price', 'telegram_profile', 'coin_name', 'coin_price']


class CoinView(ModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer


class MonitoredCoinView(ModelViewSet):
    queryset = MonitoredCoin.objects.all()
    serializer_class = MonitoredCoinSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']


