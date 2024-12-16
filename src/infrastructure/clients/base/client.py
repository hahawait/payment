import logging
import ssl
from types import TracebackType
from typing import Any, Literal, Mapping, Type

import backoff
from aiohttp import ClientError, ClientSession, TCPConnector
from ujson import dumps, loads

from infrastructure.clients.base.schemas import APIResponse


class APIClient:
    def __init__(self, base_url: str) -> None:
        self._base_url = base_url
        self._session: ClientSession | None = None
        self.log = logging.getLogger(self.__class__.__name__)

    async def _get_session(self) -> ClientSession:
        """Get aiohttp session with cache."""
        if self._session is None:
            ssl_context = ssl.SSLContext()
            connector = TCPConnector(ssl_context=ssl_context)
            self._session = ClientSession(
                base_url=self._base_url,
                connector=connector,
                json_serialize=dumps,
            )

        return self._session

    async def __aenter__(self) -> "APIClient":
        self._session = await self._get_session()
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.close()
        self._session = None

    @backoff.on_exception(
        backoff.expo,
        ClientError,
        max_time=60,
    )
    async def _make_request(
        self,
        method: Literal["GET", "POST"],
        url: str,
        json: Mapping[str, Any] | None = None,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> APIResponse:
        """
        Request with 60 seconds backoff
        :param method: Method for request GET or POST
        :param params: Query params for request
        :param json: JSON body for POST request
        :param url: would be added to base url string
        :param headers: HTTP headers for the request
        """

        async with self._session.request(method, url, params=params, json=json, headers=headers) as response:
            status = response.status
            try:
                result = await response.json(loads=loads)
            except Exception as e:
                self.log.exception(e)
                self.log.info(f"{await response.text()}")
                raise e

        return APIResponse(status=status, result=result)
