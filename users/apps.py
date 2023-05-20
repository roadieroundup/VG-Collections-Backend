from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # we need to let django know that we have signals in a different file
    def ready(self):
        import users.signals
