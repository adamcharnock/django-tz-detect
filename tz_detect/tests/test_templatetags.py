from django.test import TestCase

from tz_detect.templatetags.tz_detect import tz_detect


class TemplatetagTestCase(TestCase):
    def test_no_request_context(self):
        try:
            tz_detect({})
        except KeyError as e:
            if e.message == "request":
                self.fail("Templatetag shouldn't expect request in context.")
            else:
                raise
