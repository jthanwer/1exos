from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six


# class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         value = six.text_type(user.pk) + six.text_type(timestamp) + \
#                 six.text_type(user.is_active)
#         return value
#
#
# account_activation_token = AccountActivationTokenGenerator()
