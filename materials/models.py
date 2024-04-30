from django.db import models

from users.models import User


class Course(models.Model):
    name = models.CharField(max_length=200, verbose_name="название")
    preview = models.ImageField(
        upload_to="course_preview", verbose_name="превью", null=True, blank=True
    )
    description = models.TextField(verbose_name="описание")
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="владелец", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "курс"
        verbose_name_plural = "курсы"


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name="курс",
        related_name="lesson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=255, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(
        upload_to="lesson_preview", verbose_name="превью", null=True, blank=True
    )
    video = models.FileField(upload_to="video_lesson", blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, verbose_name="владелец", blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "урок"
        verbose_name_plural = "уроки"
