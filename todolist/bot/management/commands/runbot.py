from django.conf import settings
from django.core.management import BaseCommand
from uuid import uuid4
from todolist.bot.models import TgUser
from todolist.bot.tg.client import TgClient
from todolist.bot.tg.schemas import Message
from todolist.goals.models import Goal


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient(settings.BOT_TOKEN)

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=msg.chat.id)
        if not tg_user.user:
            # User TG is not tied to User API
            self.tg_client.send_message(msg.chat.id, 'Подтвердите, пожалуйста, свой аккаунт')
            verification_code = str(uuid4())
            tg_user.verification_code = verification_code
            tg_user.save(update_fields=['verification_code'])
            self.tg_client.send_message(msg.chat.id, f'Verification code: {verification_code}')

        else:
            # User TG is tied to User API
            self.handle_authorized_user(tg_user, msg)

    def handle_authorized_user(self, tg_user: TgUser, msg: Message):
        if msg.text.startswith('/'):
            self.handle_command(tg_user, msg.text)
        else:
            print('Неизвестная команда')

    def handle_command(self, tg_user: TgUser, command: str):
        match command:
            case '/goals':
                goals = Goal.objects.select_related('user').filter(
                    user=tg_user.user, category__is_deleted=False
                ).exclude(status=Goal.Status.archived)
                if not goals:
                    self.tg_client.send_message(tg_user.chat_id, 'No goals')
                else:
                    res = '\n'.join([goal.title for goal in goals])
                    self.tg_client.send_message(tg_user.chat_id, res)
            case '/create':
                return Goal.objects.select_related('user').filter(
                    user=tg_user.user, category__is_deleted=False
                ).exclude(status=Goal.Status.archived)
