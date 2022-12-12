def construct_with_host(host: str, path: str, **params):
    url = host.rstrip('/') + '/' + path.lstrip('/')
    if len(params) == 0:
        return url
    return url + '?' + '&'.join(map(lambda _: '{}={}'.format(_[0], _[1]), (params.items())))


def construct(url: str, **params: dict):
    if len(params) == 0:
        return url
    return url + '?' + '&'.join(map(lambda _: '{}={}'.format(_[0], _[1]), (params.items())))
