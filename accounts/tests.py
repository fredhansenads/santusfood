from django.contrib.auth import get_user_model
from django.test import SimpleTestCase

from .models import User


class UserModelConfigurationTests(SimpleTestCase):
    def test_custom_user_model_is_active(self):
        self.assertIs(get_user_model(), User)
