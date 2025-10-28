from dataclasses import dataclass


@dataclass
class ErrorTemplate:
    text: str | None = None