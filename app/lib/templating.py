from typing import Any
from app.repository import mock_crud

async def get_base_page_values() -> dict[str, Any]:
    
    best_users = await mock_crud.mock_get_users()
    popular_tags = await mock_crud.mock_get_tags()

    res = {
        "best_users": best_users, 
        "popular_tags": popular_tags,
        "user": None
    }
    return res
