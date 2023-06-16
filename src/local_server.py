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
from flask import Flask, request, render_template
from flask import send_file
from flask_cors import CORS
from loguru import logger
import base64
import os

from run import app

def return_json(data):
    return json.dumps(data, ensure_ascii=False, indent=4)

def abort(msg: str, status_code: int):
    return return_json({
        'success': False,
        'data': [],
        'msg': msg
    }), status_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    print('req', request.__dict__)
    print('files', request.files)
    print('json', request.get_json(silent=True))
    print('args', request.args)
    print('form', request.form)
    app.sendPyQtSignal(1)

    return return_json({
        'reg': str(request.__dict__),
        'files': str(request.files),
        'json': str(request.get_json(silent=True)),
        'args': str(request.args),
        'form': str(request.form)
    })

@app.route('/minimize')
@app.route('/maximize')
@app.route('/close')
def window_titlebar():
    print(request.url)
    if request.url.endswith('/minimize'):
        app.sendPyQtSignal(101)

    elif request.url.endswith('/maximize'):
        app.sendPyQtSignal(102)

    elif request.url.endswith('/close'):
        app.sendPyQtSignal(103)

    return return_json({
        'success': True
    })


if __name__ == '__main__':
    app.run(port=5001)