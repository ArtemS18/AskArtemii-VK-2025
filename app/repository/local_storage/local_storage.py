        

from pathlib import Path
from aiofiles import open
from fastapi import UploadFile

from app.core.config import config

class LocalFileStorage:
    async def connect(self) -> None:
        return None
    
    async def save_avatar(self, file: UploadFile, user_id: int) -> str:
        upload_dir = Path(config.local_storage_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        ext = Path(file.filename).suffix or ".bin"
        content = await file.read()
        filename = f"{user_id}{ext}"
        async with open(upload_dir.joinpath(filename), "bw") as f:
            await f.write(content)
        return f"http://{config.server.host}:{config.server.port}/static/avatars/{filename}"