from logging import getLogger

import asyncio
from typing import Any
import httpx


from app.lib.log import log_call

log = getLogger(__name__)

class CentrifugoCletnt():
    def __init__(self, jwt_key: str, api_key: str, api_url):
        self.jwt_key = jwt_key
        self.api_key = api_key
        self.api_url = api_url

        self.pub_queue: asyncio.Queue[dict[str, Any]] = asyncio.Queue()
        self.is_active_worker = False
        self.worker_task: asyncio.Task = None
        

    async def run_worker(self):
        self.is_active_worker = True
        self.worker_task = asyncio.create_task(self._run_worker())


    async def stop_worker(self):
        if self.is_active_worker:
            self.is_active_worker = False
        if self.worker_task:
            self.worker_task.cancel()
            try:
                await self.worker_task  
            except asyncio.CancelledError:
                print("Задача отменена")

    @log_call
    async def _fetch_pub(self, payload):
        headers = {"X-API-Key": self.api_key}
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(self.api_url, json=payload, headers=headers)
            r.raise_for_status()

    async def _run_worker(self):
        while self.is_active_worker:
            payload = await self.pub_queue.get()
            await self._fetch_pub(payload)

    @log_call
    async def publish(self, channel: str, data: dict):
        payload = {
            "method": "publish",
            "params": {"channel": channel, "data": data},
        }
        await self.pub_queue.put(payload)
        
        