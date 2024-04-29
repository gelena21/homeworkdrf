import django_filters.rest_framework
from django.shortcuts import render
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
# Create your views here.
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.serializes import PaymentSerializer, UserSerializer


class UsersAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentlListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ['course', 'lesson', 'payment_type']
    ordering_fields = ['date']
