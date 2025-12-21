from typing import Any, Callable, Coroutine, Mapping
from urllib.parse import parse_qs

async def app(scope: Mapping[str, bytes], receive: Callable[..., Coroutine[Any, Any, Mapping[str, bytes]]], send: Callable[..., Coroutine[Any, Any, None]]):
    assert scope["type"] == "http"

    method = scope["method"]

    query_string = scope.get("query_string", b"").decode()
    get_params = parse_qs(query_string)

    post_params: dict[str, str | int | None] = {}

    if method == "POST":
        body = b""
        while True:
            message = await receive()
            body += message.get("body", b"")
            if not message.get("more_body"):
                break
        post_params = parse_qs(body.decode())

    response =  (
        f"Method:\n{method}\n\n"
        f"GET params:\n{get_params}\n\n"
        f"POST params:\n{post_params}\n"
    )
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers":[
                (b"content-type", b"text/plain; charset=utf-8"),
                (b"content-length", str(len(response.encode())).encode())
            ],
        }
    )
    await send({
        "type": "http.response.body",
        "body": response.encode("utf-8"),
    })
        
        
        
