from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from todolist.core.models import User
from todolist.goals.models import Board, GoalCategory, Goal, BoardParticipant, GoalComment


class GoalApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='new_test', password='test', is_superuser=True)
        cls.test_client = Client()
        cls.response = cls.test_client.login(username='new_test', password='test')

    def create_goal(self):
        board = Board.objects.create(title='test')
        participant = BoardParticipant.objects.create(board=board, user=self.user)
        board.participants.set([participant])
        category = GoalCategory.objects.create(title='Test', board=board, user=self.user)
        goal = Goal.objects.create(title='Test_goal', category=category, user=self.user)
        return goal

    def create_comment(self):
        goal = self.create_goal()
        comment = GoalComment.objects.create(text='text', goal=goal, user=self.user)
        return comment

    def test_create_comment(self):
        url = '/goals/goal_comment/create'
        goal = self.create_goal()
        data = {'text': 'text', 'goal': goal.id, 'user': self.user}
        response = self.test_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data.get('id') == goal.id

    def test_delete_comment(self):
        comment = self.create_comment()
        url = f'/goals/goal_comment/{comment.id}'
        response = self.test_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_comments(self):
        url = '/goals/goal_comment/list'
        comment = self.create_comment()
        response = self.test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data[0].get('id') == comment.id

    def test_get_comment_by_id(self):
        comment = self.create_comment()
        url = f'/goals/goal_comment/{comment.id}'
        response = self.test_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data.get('id') == comment.id
