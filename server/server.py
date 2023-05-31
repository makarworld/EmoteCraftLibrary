import json
from flask import Flask, request
from loguru import logger
import os

try:
    from .database import ManageDB
except:
    from database import ManageDB

app = Flask(__name__)
db = ManageDB()

SKIP_AUTH = True


def return_json(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def check_access(req: request, route: str):
    # TODO: 
    #  - return it in production
    #
    # if req.headers.get('User-Agent', '').startswith('EmoteCraftLibrary/gui-client/'):
    #     return True
    
    if not req.headers.get('EMOTES-API-KEY'):
        return False, 'Missing EMOTES-API-KEY Header'
    
    elif req.headers.get('EMOTES-API-KEY'):
        if route == 'upload':
            return req.headers.get('EMOTES-API-KEY') == os.environ.get('EMOTES_API_KEY'), 'Invalid EMOTES-API-KEY Header'
        
        elif f"${route}" in req.headers.get('EMOTES-API-KEY'):
            return True, "OK"
        
        else:
            return False, 'Invalid EMOTES-API-KEY Header'
    else:
        return True, "OK"

def check_auth(func):
    def wrapper(*args, **kwargs):
        if not SKIP_AUTH:
            ok, msg = check_access(request, func.__name__)
            if not ok: return return_json({
                'success': False,
                'data': [],
                'msg': msg
            })
        return func(*args, **kwargs)
    return wrapper

@app.route('/search', methods = ['GET'])
@check_auth
def search():
    q          = request.args.get('q')
    categories = request.args.get('c')
    tags       = request.args.get('t')
    authors    = request.args.get('a')
    page       = request.args.get('p', 1)
    limit       = request.args.get('l', 9)

    if int(page) <= 0: return return_json({
        'success': False,
        'data': [],
        'msg': 'Invalid page'
    })

    categories = list(map(lambda x: x.upper().strip(), categories.split(","))) if categories else []
    tags       = list(map(lambda x: x.upper().strip(), tags.split(",")))       if tags else []
    authors    = list(map(lambda x: x.upper().strip(), authors.split(",")))    if authors else []

    logger.info(f"{q=}, {categories=}, {tags=}, {authors=}")

    result = db.search(
        query      = q, 
        categories = categories, 
        tags       = tags, 
        authors    = authors,
        page       = int(page),
        limit      = int(limit)
    )
    if not result: 
        return return_json({
            'success': True,
            'data': [],
            'msg': 'No results'
        })

    result = [x.dict() for x in result]
    
    # Your logic here
    return return_json({
        'success': True, 
        'data': result,
        'page': page,
        'limit': limit,
        'msg': ''
    })

@app.route('/download')
def download():
    uuid = request.args.get('uuid')
    # Your logic here
    return 'Download file'

@app.route('/search_pack')
def search_pack():
    q = request.args.get('q')
    categories = request.args.get('categories')
    tags = request.args.get('tags')
    # Your logic here
    return 'Search package results'

@app.route('/image/<uuid>')
def image():
    uuid = request.args.get('uuid')
    # Your logic here
    return 'Download file'

@app.route('/gif/<uuid>')
def gif():
    uuid = request.args.get('uuid')
    # Your logic here
    return 'Download file'

@app.route('/upload')
def upload():
    # get file
    file = request.args.get('file')
    os.environ.get('EMOTE_UPLOAD_KEY')
    return 'Add emote'

if __name__ == '__main__':
    app.run()