import logging
from typing import List

from starlette.requests import Request
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send

from config import settings

logger = logging.getLogger(__name__)


class BaseMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(
        self,
        scope: Scope,
        receive: Receive,
        send: Send
    ) -> None:

        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # make a request object
        request = Request(scope, receive=receive)
        ip = request.headers.get("x-real-ip", "No IP")
        request.state.ip = ip
        # pre hook
        await self.before_request(request)
        # execute
        await self.app(request.scope, request.receive, send)
        # post hook
        await self.after_response(request)

    async def before_request(self, request: Request) -> None:
        ...

    async def after_response(self, request: Request) -> None:
        ...


class LoggerMiddleware(BaseMiddleware):

    async def before_request(self, request: Request):
        logger.info(f"""
            IP: {request.state.ip}\n
            METHOD: {request.method}\n
            PATH:{request.url.path}\n
            HEADERS: {request.headers}\n
        """)


def make_middlewares() -> List[Middleware]:
    """
    :param: None
    :return: List[Middleware]
    """
    return [
        Middleware(
            CORSMiddleware,
            allow_origins=settings.CORS_ORIGINS,
            allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
            allow_methods=settings.CORS_ALLOW_METHODS,
            allow_headers=settings.CORS_ALLOW_HEADERS
        ),
        Middleware(LoggerMiddleware),
    ]
