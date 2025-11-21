import time
import asyncio
from typing import Any, Dict, Optional

import requests

# aiohttp is optional; only import if async used
try:
    import aiohttp
except ImportError:
    aiohttp = None

from .errors import ConnectifyError


def _simple_retry(func, *args, retries=2, backoff=0.5, **kwargs):
    last_exc = None
    for attempt in range(retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exc = e
            if attempt == retries:
                break
            time.sleep(backoff * (2 ** attempt))
    raise ConnectifyError(f"HTTP request failed after {retries+1} attempts: {last_exc}")


def get_json(url: str, params: Optional[Dict[str, Any]] = None, timeout: int = 10, retries: int = 2) -> Dict[str, Any]:
    def _call():
        try:
            r = requests.get(url, params=params, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except requests.RequestException as e:
            raise ConnectifyError(f"Request failed: {e}")
        except ValueError:
            raise ConnectifyError("Invalid JSON in response")

    return _simple_retry(_call, retries=retries)


class AsyncHTTPClient:
    def __init__(self, timeout: int = 10, retries: int = 2):
        if aiohttp is None:
            raise ConnectifyError("aiohttp is required for async clients. Install with: pip install aiohttp")
        self.timeout = timeout
        self.retries = retries
        self._session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if self._session:
            await self._session.close()

    async def get_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        if self._session is None:
            raise ConnectifyError("Session not initialized. Use async context manager.")
        
        last_exc = None
        backoff = 0.5
        for attempt in range(self.retries + 1):
            try:
                async with self._session.get(url, params=params, timeout=aiohttp.ClientTimeout(total=self.timeout)) as resp:
                    if resp.status != 200:
                        try:
                            data = await resp.json()
                            message = data.get("message") or str(data)
                        except Exception:
                            message = await resp.text()
                        raise ConnectifyError(f"API error ({resp.status}): {message}")
                    return await resp.json()
            except Exception as e:
                last_exc = e
                if attempt == self.retries:
                    break
                await asyncio.sleep(backoff * (2 ** attempt))
        raise ConnectifyError(f"Async HTTP request failed after {self.retries+1} attempts: {last_exc}")