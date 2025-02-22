from django.apps import AppConfig


class StickerAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sticker_app'


    def ready(self):
        import sticker_app.signals  # Import signals so they work
