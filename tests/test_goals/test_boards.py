import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db()
class TestRetrieveBoard:

    @pytest.fixture(autouse=True)
    def setup(self, board_participant):
        self.url = self.get_url(board_participant.board_id)

    @staticmethod
    def get_url(board_pk: int) -> str:
        return reverse('todolist.goals:board', kwargs={'pk': board_pk})

    def test_auth_required(self, client):
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_retrieve_deleted_doard(self, auth_client, board):
        board.is_deleted = True
        board.save(update_fields=['is_deleted'])

        response = auth_client.get(self.url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_not_board_participant(self, client, another_user):
        client.force_login(another_user)

        response = client.get(self.url)

        assert response.status_code == status.HTTP_403_FORBIDDEN
        