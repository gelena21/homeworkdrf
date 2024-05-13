import django_filters.rest_framework
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import Payment, User
from users.permissions import IsOwnerOrStaff
from users.serializes import (
    PaymentSerializer,
    UserPaymentSerializer,
    UserSerializer,
    UserSerializerCreate, PaymentApiSerializer,
)
from users.services import create_stripe_product, create_stripe_price, create_stripe_sessions, convert_rub_to_dollars


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


class PaymentApiView(CreateAPIView):
    serializer_class = PaymentApiSerializer
    queryset = Payment.objects.all()

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        product = create_stripe_product(payment.course or payment.lesson)
        price = create_stripe_price(payment.amount, product)
        session_id, payment_link = create_stripe_sessions(price)
        payment.sessions_id = session_id
        payment.link = payment_link
        payment.save()
