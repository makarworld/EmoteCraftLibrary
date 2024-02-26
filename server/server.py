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

try:
    from .database import ManageDB
    from .utils import generate_uuid
except:
    from database import ManageDB
    from utils import generate_uuid

app = Flask(__name__)
CORS(app)
db = ManageDB()

SKIP_AUTH = True
PRIVATE_ROUTES = ('upload', 'delete_emote')

def return_json(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':'))

def abort(msg: str, status_code: int):
    return return_json({
        'success': False,
        'data': [],
        'msg': msg
    }), status_code

def check_access(req, route: str):
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


@app.route('/search', methods = ['GET'])
@check_auth
def search():
    q          = request.args.get('q')
    categories = request.args.get('c')
    tags       = request.args.get('t')
    authors    = request.args.get('a')
    page       = request.args.get('p', 1)
    limit      = request.args.get('l', 9)
    print(limit)

    if int(page) <= 0: 
        return abort('Invalid page', 401)

    categories = list(map(lambda x: x.upper().strip(), categories.split(","))) if categories else []
    tags       = list(map(lambda x: x.upper().strip(), tags.split(",")))       if tags else []
    authors    = list(map(lambda x: x.strip(),         authors.split(",")))    if authors else []

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

@app.route('/info', methods = ['GET'])
@check_auth
def info():
    # count
    emotes_count = db.base.emotes.execute(
        cmd = "SELECT id FROM emotes ORDER BY id DESC LIMIT ?",
        values = (1,),
        fetchall = True
    )[0][0]

    categories_count = db.base.emotes_categories.execute(
        cmd = "SELECT id FROM emotes_categories ORDER BY id DESC LIMIT ?",
        values = (1,),
        fetchall = True
    )[0][0]

    tags_count = db.base.emotes_tags.execute(
        cmd = "SELECT id FROM emotes_tags ORDER BY id DESC LIMIT ?",
        values = (1,),
        fetchall = True
    )[0][0]

    # Your logic here
    return return_json({
        'success': True, 
        'data': [],
        'info': {
            'emotes_count': emotes_count,
            'categories_count': categories_count,
            'tags_count': tags_count
        },
        'msg': ''
    })

@app.route('/categories', methods = ['GET'])
@check_auth
def categories():
    categories = db.base.categories.execute(
        cmd = "SELECT name FROM categories",
        values = (),
        fetchall = True
    )
    categories = sorted([x[0] for x in categories])

    return return_json({
        'success': True,
        'data': categories,
        'msg': ''
    })

@app.route('/tags', methods = ['GET'])
@check_auth
def tags():
    tags = db.base.tags.execute(
        cmd = "SELECT name FROM tags",
        values = (),
        fetchall = True
    )
    tags = sorted([x[0] for x in tags])

    return return_json({
        'success': True,
        'data': tags,
        'msg': ''
    })

@app.route('/authors', methods = ['GET'])
@check_auth
def authors():
    authors = db.base.emotes.execute(
        cmd = "SELECT author FROM emotes",
        values = (),
        fetchall = True
    )
    authors = sorted(list(set([x[0] for x in authors])))

    return return_json({
        'success': True,
        'data': authors,
        'msg': ''
    })

@app.route('/emote/<uuid>', methods = ['GET'])
@check_auth
def get_emote(uuid: str):
    emote = db.base.emotes.get_one(uuid=uuid)
    if not emote:
        return abort('Not found', 404)
    

    data = {}
    for ex in ("png", "gif"):
        file = f"./server/emotes/{emote.tag}.{ex}"
        if os.path.exists(file):
            with open(file, "rb") as f:
                data[ex] = base64.b64encode(f.read()).decode('utf-8')
        else:
            data[ex] = ''
    
    with open(f"./server/emotes/{emote.tag}.json", "r", encoding="utf-8") as f:
        data['json'] = json.load(f)

    data['uuid'] = uuid

    # return file
    return return_json({
        'success': True,
        'data': data,
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

@app.route('/emote/<uuid>/delete', methods = ['GET'])
@check_auth
def delete_emote(uuid: str):
    emote = db.base.emotes.get_one(uuid=uuid)
    if not emote:
        return abort('Not found', 404)
    
    for ext in ['json', 'png', 'gif']:
        if os.path.exists(f"./server/emotes/{emote.tag}.{ext}"):
            os.remove(f"./server/emotes/{emote.tag}.{ext}")
    
    db.base.emotes.execute(
        cmd = "DELETE FROM emotes WHERE uuid = ?",
        values = (emote.uuid,)
    )

    db.base.emotes_categories.execute(
        cmd = "DELETE FROM emotes_categories WHERE eid = ?",
        values = (emote.id,)
    )

    db.base.emotes_tags.execute(
        cmd = "DELETE FROM emotes_tags WHERE eid = ?",
        values = (emote.id,)
    )

    # return file
    return return_json({
        'success': True,
        'data': [],
        'msg': ''
    })


#@app.route('/upload', methods = ['POST'])
#@check_auth
#def upload():
    # get 3 files from request
    # get json payload from request

    #print(request.files)
    #print(request.__dict__)
    #return '{}'

@app.route('/upload', methods=['POST'])
@check_auth
def upload():
    payload = request.get_json(silent=True)
    if not payload:
        return abort('Invalid payload', 400)
    
    if db.base.emotes.get_one(tag=payload['tag']):
        return abort('Tag already exists', 400)
    
    for extension in ['json', 'png', 'gif']:
        with open(f"./server/emotes/{payload['tag']}.{extension}", 'wb') as f:
            f.write(base64.b64decode(payload[extension]))

    db.base.emotes.add(
        name        = payload['name'],
        lname       = payload['name'].lower(),
        author      = payload['author'],
        description = payload['description'],
        uuid        = payload.get('uuid', generate_uuid(payload)), # !!!!
        tag         = payload['tag'],
        degrees     = payload['degrees'],
        nsfw        = payload['nsfw'],
        loop        = payload['isLoop'],
    )

    emote = db.base.emotes.get_one(tag=payload['tag'])

    for category in payload['categories']:
        if not db.base.categories.get_one(name = category):
            db.base.categories.add(name = category)

        category_id = db.base.categories.get_one(name = category).id

        db.base.emotes_categories.add(
            eid = emote.id,
            cid = category_id
        )
    
    for tag in payload['tags']:
        if not db.base.tags.get_one(name = tag):
            db.base.tags.add(name = tag)
        
        tag_id = db.base.tags.get_one(name = tag).id

        db.base.emotes_tags.add(
            eid = emote.id,
            tid = tag_id
        )

    return return_json(emote.dict())

@app.route('/test')
def test():
    print('req', request.__dict__)
    print('files', request.files)
    print('json', request.get_json(silent=True))
    print('args', request.args)
    print('form', request.form)
    return return_json({})

if __name__ == '__main__':
    app.run(port = 5020)