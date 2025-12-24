from logging import getLogger
import httpx

log = getLogger(__name__)
class CentrifugoCletnt():
    def __init__(self, jwt_key: str, api_key: str, api_url):
        self.jwt_key = jwt_key
        self.api_key = api_key
        self.api_url = api_url
        
    async def publish(self, channel: str, data: dict):
        payload = {
            "method": "publish",
            "params": {"channel": channel, "data": data},
        }
        headers = {"X-API-Key": self.api_key}
        async with httpx.AsyncClient(timeout=3.0) as client:
            r = await client.post(self.api_url, json=payload, headers=headers)
            r.raise_for_status()
            log.info(r.json())