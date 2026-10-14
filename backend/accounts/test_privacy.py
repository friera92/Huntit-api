import logging

from django.test import TestCase

from config_pkg.privacy import RedactQueryFilter


class PrivacyTests(TestCase):
    def test_account_and_personal_responses_are_not_cached(self):
        for path in ("/api/auth/me/", "/api/auth/csrf/", "/api/personal/preferences/"):
            response = self.client.get(path)
            self.assertIn("no-store", response["Cache-Control"])
            self.assertIn("Cookie", response["Vary"])
            self.assertEqual(response["Referrer-Policy"], "no-referrer")

    def test_access_logs_redact_search_and_license_query_values(self):
        record = logging.LogRecord("django.server", logging.INFO, "", 0, "%s %s %s", (
            "GET /api/regulations/search/?species=4&date=2026-10-12&managed_area=17 HTTP/1.1", 200, 400,
        ), None)
        RedactQueryFilter().filter(record)
        self.assertEqual(record.getMessage(), "GET /api/regulations/search/?[redacted] HTTP/1.1 200 400")
        record = logging.LogRecord("django.request", logging.WARNING, "", 0,
                                   "Bad request: /api/personal/licenses/?notes=private-license", (), None)
        RedactQueryFilter().filter(record)
        self.assertNotIn("private-license", record.getMessage())
