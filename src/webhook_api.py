import httpx
import re

import typing as t


class WebhookManagerError(Exception):
    pass


class WebhookIsNotValid(WebhookManagerError):
    pass


class WebhookDoesNotExist(WebhookManagerError):
    pass


WRONG_WEBHOOK_TYPES = (WebhookDoesNotExist, WebhookIsNotValid)


def exists_decorator(func):
    def wrap(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise WebhookDoesNotExist
            raise e
    return wrap


class WebHookManager:
    WEBHOOK_URL_RE = re.compile(r"https?://(?:www\.|ptb\.|canary\.)?discord(?:app)?\.com/api(?:/v\d+)?/webhooks/\d+/[\w-]+(?:\?thread_id=\d+)?")

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url
        self.valid()
        self.exists()

    def valid(self):
        if not self.WEBHOOK_URL_RE.match(self.webhook_url):
            raise WebhookIsNotValid()
        return True

    def exists(self):
        try:
            req = httpx.get(self.webhook_url)
            req.raise_for_status()
            return True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                raise WebhookDoesNotExist
            raise e

    @exists_decorator
    def get_raw_json_info(self):
        req = httpx.get(self.webhook_url)
        req.raise_for_status()
        return req.json()

    @exists_decorator
    def delete(self):
        req = httpx.delete(self.webhook_url)
        req.raise_for_status()

    @exists_decorator
    def send(self, content: t.Optional[str] = None, username: t.Optional[str] = None, avatar_url: t.Optional[str] = None,
             embeds: t.Optional[t.Iterable] = None, files: t.Optional[tuple] = None):
        if not any((content is not None, embeds is not None)):
            raise ValueError("content or embeds required")
        data = dict(filter(lambda x: x[1] is not None, dict(content=content, username=username, avatar_url=avatar_url,
                                                            embeds=embeds, files=files).items()))
        req = httpx.post(self.webhook_url, json=data)
        req.raise_for_status()
