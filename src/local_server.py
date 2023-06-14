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

GET /info
Return info about server

GET /categories
Return all categories

GET /authors
Return all authors

GET /tags
Return all tags

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
from flask_cors import CORS
from loguru import logger
import base64
import os

app = Flask(__name__)
CORS(app)

SKIP_AUTH = True
PRIVATE_ROUTES = ('upload', 'delete_emote')

def return_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)

def abort(msg: str, status_code: int):
    return return_json({
        'success': False,
        'data': [],
        'msg': msg
    }), status_code

def check_access(req: request, route: str):
    if req.headers.get('User-Agent', '').startswith('EmoteCraftLibrary/gui-client/'):
        return True, "OK"

    if not req.headers.get('EMOTES-API-KEY'):
        return False, 'Missing EMOTES-API-KEY Header'
    
    elif req.headers.get('EMOTES-API-KEY'):
        is_admin = req.headers.get('EMOTES-API-KEY') == os.environ.get('EMOTES_API_KEY')

        if route in PRIVATE_ROUTES:
            return is_admin, 'Invalid EMOTES-API-KEY Header'
        
        elif req.headers.get('EMOTES-API-KEY') == "$public-api-key$" or is_admin:
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
    
    # fix error with decorator and flask route
    wrapper.__name__ = func.__name__

    return wrapper

@app.route('/test')
def test():
    print('req', request.__dict__)
    print('files', request.files)
    print('json', request.get_json(silent=True))
    print('args', request.args)
    print('form', request.form)

    return return_json({
        'reg': str(request.__dict__),
        'files': str(request.files),
        'json': str(request.get_json(silent=True)),
        'args': str(request.args),
        'form': str(request.form)
    })

if __name__ == '__main__':
    app.run(port=5001)