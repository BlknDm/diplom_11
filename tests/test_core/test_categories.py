from rest_framework.test import APITestCase
from django.test import Client
from rest_framework import status
from todolist.core.models import User
from todolist.goals.models import Board, BoardParticipant, GoalCategory


class TestGoalCategory(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='new_test', password='test', is_superuser=True)
        cls.test_client = Client()
        cls.response = cls.test_client.login(username='new_test', password='test')

    def create_board(self):
        board = Board.objects.create(title='test')
        participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([participant])
        return board

    def category_create(self):
        board = self.create_board()
        category = GoalCategory.objects.create(title='test', board=board, user=self.user)
        return category

    def test_create_goal_category(self):
        url = '/goals/goal_category/create'
        board = self.create_board()
        title = 'goal'
        response = self.test_client.post(url, {'title': title, 'board': board.id})
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('title') == title

    def test_goal_category_delete(self):
        category = self.category_create()
        url = f'/goals/goal_category/{category.id}'
        response = self.test_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert GoalCategory.objects.get(id=category.id).is_deleted

    def test_list_goal_category(self):
        url = '/goals/goal_category/list'
        category = self.category_create()
        response = self.test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0]['id'] == category.id
