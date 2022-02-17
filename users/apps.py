from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    def ready(sellf):
        import users.signals

# class OtpCodeConfig(AppConfig):
#     name = 'otp'

#     def ready(self):
#        import users.signals