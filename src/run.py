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
from flask import Flask
from flask_cors import CORS

from pyfladesk import init_gui

from local_server import *

app = Flask(__name__)
CORS(app)


if __name__ == '__main__':
    init_gui(app, 5010, 1280, 688)