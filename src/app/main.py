# import python libs


from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from postal.parser import parse_address
from postal.expand import expand_address

app = FastAPI()

app.add_middleware(GZipMiddleware)


def camel(snake_str):
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def parse_internal(address):
    result = {}
    for item in parse_address(address):
        result[camel(item[1])] = item[0]
    return result


@app.get('/')
def index():
    return {'version': 'v1.0.0'}


@app.get('/parse')
def parse(address: str):

    if not address:
        return {'error': 'address required'}, 400

    return parse_internal(address)


@app.get('/expand')
def expand(address: str):

    if not address:
        return {'error': 'address required'}, 400

    return expand_address(address)


@app.get('/explode')
def explode(address: str):

    if not address:
        return {'error': 'address required'}, 400

    results = [parse_internal(address)]

    for item in expand_address(address):
        results.append(parse_internal(item))

    return results
