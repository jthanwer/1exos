from django.apps import AppConfig


class filemanagerConfig(AppConfig):
    name = 'filemanager'

    def ready(self):
        import filemanager.signals
