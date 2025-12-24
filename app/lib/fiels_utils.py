

from pathlib import Path
from fastapi import UploadFile


MAX_FILE_SIZE = 1024*1024*5

class MaxFileSizeError(Exception):
    ...

class EmptyFileError(Exception):
    ...

class UnexeptSizeError(Exception):
    ...

class NotValidPostfix(Exception):
    ...



async def get_size(file: UploadFile):
    if size := file.size:
        return size
    if size :=  file.headers.get("content-length"):
        print(size)
        return int(size)
    else:
        size = 0
        while True:
            chunk = await file.read(size=8192)
            
            if not chunk:
                break

            size += len(chunk)

        await file.seek(0)
        return size

async def validata_file(file: UploadFile):
    file_size = await get_size(file)
    print(file_size)
    if file_size > MAX_FILE_SIZE:
        raise MaxFileSizeError
    elif file_size == 0:
        raise EmptyFileError
    
    ext = Path(file.filename).suffix or ".bin"
    if ext not in (".jpeg", ".jpg", ".png", ".svg"):
        raise NotValidPostfix
