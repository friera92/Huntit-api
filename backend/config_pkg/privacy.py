"""Keep account responses out of caches and private query values out of logs."""
import logging
import re

from django.utils.cache import patch_vary_headers


class RedactQueryFilter(logging.Filter):
    _query = re.compile(r"((?:https?://|/)[^\s?'\"<>]*)\?[^\s'\"<>]*")

    @classmethod
    def redact(cls, value):
        if isinstance(value, str):
            return cls._query.sub(r"\1?[redacted]", value)
        return value

    def filter(self, record):
        record.msg = self.redact(record.msg)
        if isinstance(record.args, dict):
            record.args = {key: self.redact(value) for key, value in record.args.items()}
        elif record.args:
            record.args = tuple(self.redact(value) for value in record.args)
        return True


class PrivateResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(("/api/auth/", "/api/personal/", "/admin/")):
            response["Cache-Control"] = "private, no-store"
            patch_vary_headers(response, ("Cookie",))
        response["Referrer-Policy"] = "no-referrer"
        return response
