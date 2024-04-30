import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsOwnerOrStaff
from users.serializes import (PaymentSerializer, UserPaymentSerializer,
                              UserSerializer, UserSerializerCreate)


class UsersPaymentsAPIViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserPaymentSerializer


class PaymentlListView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter, django_filters.rest_framework.DjangoFilterBackend]

    filterset_fields = ["course", "lesson", "payment_type"]
    ordering_fields = ["date"]


class UserListAPIView(ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializerCreate
    queryset = User.objects.all()
    permission_classes = [AllowAny]


class UserRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrStaff]
