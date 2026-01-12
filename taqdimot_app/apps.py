from django.apps import AppConfig
import os
import threading


class TaqdimotAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'taqdimot_app'

    def ready(self):
        # runserver autoreload sababli 2 marta ishga tushmasligi uchun
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from bot import start_bot

        threading.Thread(
            target=start_bot,
            daemon=True
        ).start()


# from django.apps import AppConfig


# class TaqdimotAppConfig(AppConfig):
#     name = 'taqdimot_app'
