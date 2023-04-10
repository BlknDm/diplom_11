from typing import Any

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.request import Request

from todolist.goals.models import Board, BoardParticipant, GoalCategory, GoalComment


class BoardPermissions(IsAuthenticated):
    def has_object_permission(self, request: Request, view, obj: Board) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': obj.id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class GoalCategoryPermissions(IsAuthenticated):
    def has_object_permission(self, request: Request, view, goal_category: GoalCategory) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': goal_category.board_id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()


class CommentPermissions(IsAuthenticated):
    def has_object_permission(self, request: Request, view, goal_comment: GoalComment) -> bool:
        _filters: dict[str: Any] = {'user_id': request.user.id, 'board_id': goal_comment.goal_id}
        if request.method not in SAFE_METHODS:
            _filters['role'] = BoardParticipant.Role.owner

        return BoardParticipant.objects.filter(**_filters).exists()
