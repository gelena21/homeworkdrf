from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="test@study.com",
            first_name="Admin",
            last_name="Biggest",
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        user.set_password("2182")
        user.save()

        self.stdout.write(
            self.style.SUCCESS("создан суперпользователь\n" "test@study.com\n" "2182")
        )
