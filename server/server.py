"""
ENDPOINTS

GET /search
parameters:
    q: str # query
    c: str # comma separated list of categories
    t: str # comma separated list of tags
    a: str # comma separated list of authors
    p: int # page
    l: int # limit

## EMOTE
### Client-Side

GET /emote/<uuid>/downdload
Download zip file of emotes, contain .json, .png, .gif files

GET /emote/<uuid>/png
Get emote image

GET /emote/<uuid>/gif
Get emote gif

GET /emote/<uuid>/json
Get emote json

### Admin-Side

GET /emote/<uuid>/update/png
REQUIRED: EMOTES-API-KEY (admin)
Update emote image

GET /emote/<uuid>/update/gif
REQUIRED: EMOTES-API-KEY (admin)
Update emote gif

GET /emote/<uuid>/update/json
REQUIRED: EMOTES-API-KEY (admin)
Update emote json

GET /emote/<uuid>/delete
REQUIRED: EMOTES-API-KEY (admin)
Delete emote

### OTHER

GET /upload
Upload emote zip-file with .json, .png, .gif
REQUIRED: EMOTES-API-KEY api-key
WARNING: .json file shound contain key 'comment': "*::metadata-start:CATEGORIES: ... ::TAGS: ... ::metadata-end:".
         CATEGORIES and TAGS should me strings separated by comma.

## EMOTE-PACK

SOON

GET /search_pack

SOON


"""
import json
from flask import Flask, request
from flask import send_file
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

def abort(msg: str, status_code: int):
    return return_json({
        'success': False,
        'data': [],
        'msg': msg
    }), status_code

def check_access(req: request, route: str):
    if req.headers.get('User-Agent', '').startswith('EmoteCraftLibrary/gui-client/'):
        return True

    if not req.headers.get('EMOTES-API-KEY'):
        return False, 'Missing EMOTES-API-KEY Header'
    
    elif req.headers.get('EMOTES-API-KEY'):
        is_admin = req.headers.get('EMOTES-API-KEY') == os.environ.get('EMOTES_API_KEY')

        if route == 'upload':
            return is_admin, 'Invalid EMOTES-API-KEY Header'
        
        elif f"$public-api-key$" in req.headers.get('EMOTES-API-KEY') or is_admin:
            return True, "OK"
        
        else:
            return False, 'Invalid EMOTES-API-KEY Header'
    else:
        return True, "OK"

def check_auth(func):
    def wrapper(*args, **kwargs):
        if not SKIP_AUTH:
            ok, msg = check_access(request, func.__name__)
            if not ok: 
                abort(msg, 401)
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
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

    if int(page) <= 0: 
        return abort('Invalid page', 401)

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

@app.route('/emote/<uuid>/png', methods = ['GET'])
@check_auth
def download_png(uuid: str):
    emote = db.base.emotes.get_one(uuid=uuid)
    if not emote:
        return abort('Not found', 404)
    
    if not os.path.exists(f"./server/emotes/{emote.tag}.png"):
        return abort('Not found image on server', 404)
    
    # return file
    return send_file(f"emotes\\{emote.tag}.png", mimetype='image/gif')

@app.route('/emote/<uuid>/gif', methods = ['GET'])
@check_auth
def download_gif(uuid: str):
    emote = db.base.emotes.get_one(uuid=uuid)
    if not emote:
        return abort('Not found', 404)
    
    if not os.path.exists(f"./server/emotes/{emote.tag}.gif"):
        return abort('Not found gif on server', 404)
    
    # return file
    return send_file(f"emotes\\{emote.tag}.gif", mimetype='image/gif')

@app.route('/emote/<uuid>/json', methods = ['GET'])
@check_auth
def download_json(uuid: str):
    emote = db.base.emotes.get_one(uuid=uuid)
    if not emote:
        return abort('Not found', 404)
    
    if not os.path.exists(f"./server/emotes/{emote.tag}.json"):
        return abort('Not found gif on server', 404)
    
    # return file
    return send_file(f"emotes\\{emote.tag}.json")

if __name__ == '__main__':
    app.run()