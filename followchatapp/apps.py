from django.apps import AppConfig


class FollowchatappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'followchatapp'

    def ready(self):
        import followchatapp.signals
