from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="email")
    avatar = models.ImageField(
        upload_to="users/", verbose_name="аватар", blank=True, null=True
    )
    phone_number = models.CharField(
        max_length=35, verbose_name="номер телефона", blank=True, null=True
    )
    city = models.CharField(max_length=150, verbose_name="город", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    class PaymentType(models.TextChoices):
        CASH = "cash", "наличные"
        SPENDING = "spending", "перевод на счет"

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="user",
        verbose_name="пользователь",
        null=True,
        blank=True,
    )
    date = models.DateField(auto_now=True, verbose_name="дата оплаты")
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный курс",
        null=True,
        blank=True,
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        verbose_name="оплаченный урок",
        null=True,
        blank=True,
    )
    amount = models.PositiveIntegerField(verbose_name="сумма оплаты")
    payment_type = models.CharField(
        max_length=28, choices=PaymentType.choices, verbose_name="способ оплаты"
    )
    sessions_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="id сессии",
        help_text="укажите id сессии",
    )
    link = models.URLField(
        max_length=400,
        blank=True,
        null=True,
        verbose_name="ссылка на оплату",
        help_text="укажите ссылку на оплату",
    )

    class Meta:
        verbose_name = "оплата"
        verbose_name_plural = "оплаты"
        ordering = ("user", "date")

    def __str__(self):
        return (
            f"Пользователь: {self.user}\n"
            f"Курс:  {self.course}\n"
            f"Сумма: {self.amount}"
        )
