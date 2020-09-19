from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django.core.files.storage import FileSystemStorage
import os

if os.environ.get('USE_S3') == "TRUE" and not settings.DEBUG:
    class StaticStorage(S3Boto3Storage):
        location = settings.AWS_STATIC_LOCATION
        default_acl = 'public-read'

    class PublicMediaStorage(S3Boto3Storage):
        location = settings.AWS_PUBLIC_MEDIA_LOCATION
        default_acl = 'public-read'
        file_overwrite = False

    class PrivateMediaStorage(S3Boto3Storage):
        location = settings.AWS_PRIVATE_MEDIA_LOCATION
        default_acl = 'private'
        file_overwrite = False
        custom_domain = False

elif os.environ.get('USE_S3') == "TRUE" and settings.DEBUG:
    class StaticStorage(S3Boto3Storage):
        location = settings.AWS_STATIC_LOCATION
        default_acl = 'public-read'

    class PublicMediaStorage(S3Boto3Storage):
        location = 'media_test/public'
        default_acl = 'public-read'
        file_overwrite = False

    class PrivateMediaStorage(S3Boto3Storage):
        location = 'media_test/private'
        default_acl = 'private'
        file_overwrite = False
        custom_domain = False

else:
    class PrivateMediaStorage(FileSystemStorage):
        pass

