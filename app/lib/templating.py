from typing import Any
from app.repository import crud

async def get_base_page_values() -> dict[str, Any]:
    
    best_users = await crud.mock_get_users()
    popular_tags = await crud.mock_get_tags()

    res = {
        "best_users": best_users, 
        "popular_tags": popular_tags,
        "user": None
    }
    return res
