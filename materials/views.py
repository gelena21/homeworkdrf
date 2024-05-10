from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    get_object_or_404,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, CourseSubscription
from materials.paginations import LessonPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializes import (
    CourseSerializer,
    LessonSerializer,
    CourseSubscriptionSerializer,
)


class CourseAPIViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LessonPaginator
    permission_classes = [
        IsAuthenticated,
    ]

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [IsAuthenticated, ~IsModerator]
        elif self.action == "list":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "retrieve":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "update":
            self.permission_classes = [IsAuthenticated, IsOwner | IsModerator]
        elif self.action == "destroy":
            self.permission_classes = [IsAuthenticated, IsOwner]
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        my_queryset = Course.objects.all()
        if not self.request.user.is_moderator:
            my_queryset = my_queryset.owner(self.request.user)
        return my_queryset


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

    def perform_create(self, serializer):
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = LessonPaginator
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        if self.request.user.groups.filter(name="moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class SubscribtionCourseAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get("course")
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item, created = CourseSubscription.objects.get_or_create(
            user=user, course=course_item
        )

        if created:
            message = "подписка добавлена"
        else:
            subs_item.delete()
            message = "подписка удалена"

        return Response(message)
