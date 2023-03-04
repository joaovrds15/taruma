from django.apps import AppConfig
from django.conf import settings
from .s3 import S3Uploader


class CatalogoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'catalogo'

    def ready(self):
        bucket_name = settings.AWS_BUCKET_NAME
        access_key = settings.AWS_SECRET_ACCESS_KEY
        access_key_id = settings.AWS_ACCESS_KEY_ID
        uploader = S3Uploader(bucket_name, access_key_id, access_key)
        self.uploader = uploader
    
default_app_config = 'catalogo.CatalogoConfig'