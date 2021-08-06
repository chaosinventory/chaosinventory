from django.apps import AppConfig


class BaseConfig(AppConfig):
    # See https://stackoverflow.com/a/67057826/11249686
    name = 'chaosinventory.base'
    # Introduced in the Django3.2 update, BigAutoField is the
    # new default and should not break anything for us
    default_auto_field = 'django.db.models.BigAutoField'
