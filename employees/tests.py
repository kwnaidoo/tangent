# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from django.test import TestCase
from datetime import datetime, timedelta
from employees.templatetags.employee_tags import get_birthday


class APITestCase(TestCase):

    # test the future birthday calculation
    def test_employee_tags(self):
        future_birth_date = get_birthday(3)
        self.assertEqual(
            "{:%d, %b %Y}".format(datetime.now() + timedelta(days=3)),
            future_birth_date
        )

    # test that unauthenticated users are redirected to the login screen
    def test_authentication(self):
        response = self.client.get("/", follow=True)
        self.assertRedirects(response, '/login/')
