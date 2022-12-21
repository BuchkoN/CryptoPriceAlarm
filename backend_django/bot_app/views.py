from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from bot_app.models import TelegramProfile


class TelegramProfileSerializer(ModelSerializer):
    class Meta:
        model = TelegramProfile
        fields = ['id', 'user_id', 'username']


class TelegramProfileView(ModelViewSet):
    queryset = TelegramProfile.objects.all()
    serializer_class = TelegramProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_id']