from urllib.parse import parse_qs


def app(environ, start_response):
    method = environ.get("REQUEST_METHOD", "GET")

    get_params = parse_qs(environ.get("QUERY_STRING", ""))

    post_params = {}
    if method == "POST":
        try:
            content_length = int(environ.get("CONTENT_LENGTH", 0))
        except (ValueError, TypeError):
            content_length = 0

        body = environ["wsgi.input"].read(content_length).decode("utf-8")
        post_params = parse_qs(body)

    response_body = (
        "Method:\n"
        f"{method}\n\n"
        "GET params:\n"
        f"{get_params}\n\n"
        "POST params:\n"
        f"{post_params}\n"
    )

    start_response(
        "200 OK",
        [
            ("Content-Type", "text/plain; charset=utf-8"),
            ("Content-Length", str(len(response_body.encode("utf-8")))),
        ],
    )

    return [response_body.encode("utf-8")]
