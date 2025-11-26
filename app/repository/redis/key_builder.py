
BASE_KEY = "app:"

def get_session_key(key: str) -> str:
    return f"{BASE_KEY}users:session:{key}"


