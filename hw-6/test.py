# curl -X GET 'http://127.0.0.1:8081?a=1&b=2'
# curl -X POST 'http://127.0.0.1:8081?a=1&b=2'


def simple_app(environ, start_response):
    print(environ['REQUEST_METHOD'])
    print(environ['QUERY_STRING'])
    params = ', '.join([param.split('=')[0] for param in environ['QUERY_STRING'].split('&')])
    data = b"Hello, World!\n" \
           + environ['REQUEST_METHOD'].encode() \
           + "\n".encode() \
           + params.encode() \
           + "\n".encode()
    start_response("200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])
    return [data]
