import json

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase

User = get_user_model()
PASSWORD = "A-strong-unique-passphrase-674!"


class AuthenticationTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client(enforce_csrf_checks=True)

    def post(self, path, data, with_csrf=True):
        headers = {}
        if with_csrf:
            self.client.get("/api/auth/csrf/")
            headers["HTTP_X_CSRFTOKEN"] = self.client.cookies["csrftoken"].value
        return self.client.post(path, json.dumps(data), content_type="application/json", **headers)

    def register(self, **extra):
        data = {"username": "testhunter", "email": "testhunter@example.com", "password": PASSWORD, "password_confirm": PASSWORD}
        data.update(extra)
        return self.post("/api/auth/register/", data)

    def test_registration_hashes_password_and_starts_session(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        user = User.objects.get(username="testhunter")
        self.assertNotEqual(user.password, PASSWORD)
        self.assertTrue(user.check_password(PASSWORD))
        self.assertNotIn("password", response.json())
        self.assertFalse(user.is_staff)
        self.assertEqual(self.client.get("/api/auth/me/").json()["id"], user.pk)

    def test_user_cannot_choose_staff_privileges_on_registration(self):
        self.assertEqual(self.register(is_staff=True, is_superuser=True).status_code, 201)
        user = User.objects.get(username="testhunter")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_weak_mismatched_and_duplicate_registration_are_rejected(self):
        self.assertEqual(self.register(password="password", password_confirm="password").status_code, 400)
        self.assertEqual(self.register(password_confirm="different").status_code, 400)
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(self.register().status_code, 201)
        self.assertEqual(self.register().status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_login_logout_and_wrong_credentials(self):
        user = User.objects.create_user(username="testhunter", password=PASSWORD)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
        self.assertEqual(self.post("/api/auth/login/", {"username": "testhunter", "password": "wrong"}).status_code, 400)
        self.assertEqual(self.post("/api/auth/login/", {"username": "testhunter", "password": PASSWORD}).status_code, 200)
        old_session = self.client.cookies["sessionid"].value
        self.assertEqual(self.client.get("/api/auth/me/").json()["id"], user.pk)
        self.assertEqual(self.post("/api/auth/logout/", {}).status_code, 204)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 401)
        old_client = Client()
        old_client.cookies["sessionid"] = old_session
        self.assertEqual(old_client.get("/api/auth/me/").status_code, 401)

    def test_anonymous_auth_posts_require_csrf(self):
        self.assertEqual(self.register_without_csrf().status_code, 403)
        self.assertEqual(self.post("/api/auth/login/", {"username": "testhunter", "password": PASSWORD}, with_csrf=False).status_code, 403)
        self.assertEqual(User.objects.count(), 0)

    def register_without_csrf(self):
        return self.post("/api/auth/register/", {"username": "testhunter", "email": "testhunter@example.com", "password": PASSWORD, "password_confirm": PASSWORD}, with_csrf=False)

    def test_session_logout_requires_csrf_and_rotates_token_on_login(self):
        self.client.get("/api/auth/csrf/")
        before = self.client.cookies["csrftoken"].value
        self.register()
        self.assertNotEqual(before, self.client.cookies["csrftoken"].value)
        self.assertEqual(self.post("/api/auth/logout/", {}, with_csrf=False).status_code, 403)
        self.assertEqual(self.client.get("/api/auth/me/").status_code, 200)

    def test_inactive_user_cannot_log_in(self):
        User.objects.create_user(username="testhunter", password=PASSWORD, is_active=False)
        self.assertEqual(self.post("/api/auth/login/", {"username": "testhunter", "password": PASSWORD}).status_code, 400)

    def test_authentication_attempts_are_throttled(self):
        for _ in range(20):
            self.assertEqual(self.post("/api/auth/login/", {"username": "unknown", "password": PASSWORD}).status_code, 400)
        self.assertEqual(self.post("/api/auth/login/", {"username": "unknown", "password": PASSWORD}).status_code, 429)
