from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.views import (
    CourseAPIViewSet,
    LessonCreateAPIView,
    LessonDestroyAPIView,
    LessonListAPIView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
    SubscribtionCourseAPIView,
)

router = DefaultRouter()
router.register("course", CourseAPIViewSet)

urlpatterns = [
    path("lessons/", LessonListAPIView.as_view(), name="lessons_list"),
    path("lesson/create/", LessonCreateAPIView.as_view(), name="lesson_create"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/<int:pk>/detail/", LessonRetrieveAPIView.as_view(), name="lesson_detail"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_destroy"
    ),
    path("subscription/", SubscribtionCourseAPIView.as_view(), name="subscription"),
]

urlpatterns += router.urls
