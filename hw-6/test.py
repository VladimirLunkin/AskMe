import gunicorn.app.base
resp_html = b"""<html lang="en">
<head>
<meta charset="UTF-8">
    <title>Test</title>
</head>
<body>
    <a href="/?a7"><button>GET</button></a>
    <form method="post">
        <p><input name="data">
        <button type="submit">POST</button>
    </form>
</body>
</html>"""


def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    print(environ['REQUEST_METHOD'])
    print(environ['QUERY_STRING'])
    print(environ)
    return [resp_html]
