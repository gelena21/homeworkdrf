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
        response = self.client.get('/materials/lessons/')
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
            f'/materials/lesson/{les_detail.id}/detail/')

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
            f'/materials/lesson/{lesson.id}/update/',
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
            f'/materials/lesson/{lesson.id}/delete/',
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

        response = self.client.post('/materials/subscription/', data=data)

        self.assertEquals(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEquals(
            response.json(),
            'подписка добавлена'
        )
