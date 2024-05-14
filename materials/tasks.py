from celery import shared_task
from config import settings
from django.core.mail import send_mail
from materials.models import Course, CourseSubscription


@shared_task
def send_info_about_update_course(course_id):
    print("Отправка письма")
    course = Course.objects.get(pk=course_id)
    course_users = CourseSubscription.objects.filter(course=course_id)
    for user in course_users:
        send_mail(
            subject=f"{course.name}",
            message=f'Есть новое обновление "{course.name}"',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[f"{user.user}"],
            fail_silently=True,
        )
