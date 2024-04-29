import datetime

from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    help = ''

    def handle(self, *args, **kwargs):
        Payment.objects.all().delete()

        user1, created = User.objects.get_or_create(email='user1@test.ru')
        user2, created = User.objects.get_or_create(email='user2@test.ru')

        course1, created = Course.objects.get_or_create(name='Курс 1')
        course2, created = Course.objects.get_or_create(name='Курс 2')

        lesson1, created = Lesson.objects.get_or_create(name='Урок 1')
        lesson2, created = Lesson.objects.get_or_create(name='Урок 2')

        payment1 = Payment.objects.create(
            user=user1,
            date=datetime.datetime.now().date,
            amount=170,
            payment_type='cash',
            course=course1)

        payment2 = Payment.objects.create(
            user=user2,
            date=datetime.datetime.now().date,
            amount=356,
            payment_type='spend',
            course=course2)

        payment3 = Payment.objects.create(
            user=user1,
            date=datetime.datetime.now().date,
            amount=789,
            payment_type='cash',
            lesson=lesson1, )

        payment4 = Payment.objects.create(
            user=user2,
            date=datetime.datetime.now().date,
            amount=834,
            payment_type='spend',
            lesson=lesson1, )

        self.stdout.write(self.style.SUCCESS("тестирование"
                                             "загружено"))
