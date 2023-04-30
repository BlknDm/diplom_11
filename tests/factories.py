import factory
from pytest_factoryboy import register

from todolist.core.models import User
from todolist.goals.models import Board, BoardParticipant


@register
class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return User.objects.create_user(*args, **kwargs)


class DateTimeMixin(factory.django.DjangoModelFactory):
    class Meta:
        abstract = True


@register
class BoardFactory(DateTimeMixin):
    title = factory.Faker('catch_phrase')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(board=self, user=owner, role=BoardParticipant.Role.owner)


@register
class BoardParticipantFactory(DateTimeMixin):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant
