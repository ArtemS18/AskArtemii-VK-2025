import re

def parse_tags(raw: str | None, *, max_len: int = 100, max_tags: int = 10) -> list[str]:
    if not raw:
        return []
    parts = re.split(r"[\s,]+", raw.strip())
    seen: set[str] = set()
    out: list[str] = []
    for p in parts:
        name = p.strip().lower()
        if not name:
            continue
        name = name[:max_len]
        if name in seen:
            continue
        seen.add(name)
        out.append(name)
        if len(out) >= max_tags:
            break
    return out