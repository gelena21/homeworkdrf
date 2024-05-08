from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from materials.models import Lesson, Course
from users.models import User


class LessonsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            email='example@example.com',
            is_superuser=True,
            is_staff=True,
        )
        self.user.set_password('2182')
        self.client.force_authenticate(user=self.user)

        Lesson.objects.create(
            owner=self.user,
            name='begining',
            description='description',
            video='youtube.com/watch/000'
        )

    def test_create_lesson(self):
        """CREATE TEST"""
        data = {'name': 'test', 'description': 'test description'}
        url = reverse('lesson_create')
        response = self.client.post(url, data=data)
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_list_lesson(self):
        url = reverse('lesson_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': 7,
                'name': 'begining',
                'description': 'description',
                'preview': None,
                'video': 'http://testserver/youtube.com/watch/000',
                'course': None,
                'owner': 4}]})

    def test_detail_lesson(self):
        les_detail = Lesson.objects.create(
            owner=self.user,
            name='detail',
            description='description',
            video='youtube.com/watch/123456'
        )

        response = self.client.get(
            reverse('lesson_detail',
                    args=[les_detail.id])
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.json(), {
            'id': 6,
            'name': 'detail',
            'description': 'description',
            'preview': None,
            'video': 'http://testserver/youtube.com/watch/123456',
            'course': None, 'owner': 3})

    def test_update_lesson(self):
        lesson = Lesson.objects.create(
            owner=self.user,
            name='updating',
            description='old_one description',
            video='youtube.com/watch/1234'
        )

        response = self.client.patch(
            reverse('lesson_update', args=[lesson.id]),
            data={'name': 'new_testing_name'}
        )

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_lesson(self):
        lesson = Lesson.objects.create(
            owner=self.user,
            name='deleting',
            description='description',
            video='youtube.com/watch/3456'
        )

        response = self.client.delete(
            reverse('lesson_destroy', args=[lesson.id]),
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.ru",
            is_staff=True,
            is_active=True,
            is_superuser=False,
        )
        self.user.set_password("1234")
        self.user.save()

        self.course = Course.objects.create(
            name="course 1",
            description="testing",
            owner=self.user
        )

        self.client.force_authenticate(user=self.user)

    def test_subscribe_to_course(self):
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }

        url = reverse('subscription')
        response = self.client.post(url, data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            'подписка добавлена'
        )
