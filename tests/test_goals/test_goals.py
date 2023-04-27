from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from todolist.core.models import User
from todolist.goals.models import Board, GoalCategory, Goal, BoardParticipant


class GoalApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='user_test', password='test', is_superuser=True)
        cls.test_client = Client()
        cls.response = cls.test_client.login(username='user_test', password='test')

    def create_category(self):
        board = Board.objects.create(title='test')
        participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([participant])
        category = GoalCategory.objects.create(title='category', board=board, user=self.user)
        return category

    def create_goal(self):
        category = self.create_category()
        goal = Goal.objects.create(title='goal', category=category, user=self.user)
        return goal

    def test_goal_create(self):
        url = '/goals/goal/create'
        category = self.create_category()
        data = {'title': 'test', 'category': category.id, 'user': self.user}
        response = self.test_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('title') == 'test'

    def test_goal_delete(self):
        goal = self.create_goal()
        self.assertEqual(goal.status, 1)
        url = f'/goals/goal/{goal.id}'
        response = self.test_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Goal.objects.get(id=goal.id).status == 4

    def test_lists_goals(self):
        url = '/goals/goal/list'
        goal = self.create_goal()
        response = self.test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0].get('id') == goal.id

    def test_goal_get(self):
        goal = self.create_goal()
        url = f'/goals/goal/{goal.id}'
        response = self.test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == goal.id
