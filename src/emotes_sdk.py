import json
import os
from typing import List
import requests
import base64

from utils import Singleton

class BaseSDK:
    def __init__(self, api_key: str = None, test: bool = True):
        self.api_key = api_key
        self.test = test

        #if self.test:
        self.url = "http://127.0.0.1:5000"

        self.session = requests.Session()
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'EmoteCraftLibrary/gui-client/0.0.1',
            'EMOTES-API-KEY': self.api_key if self.api_key else "$public-api-key$",
        })

    def call(self, method: str, endpoint: str, raw = False, **kwargs):
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"

        response = self.session.request(method, f"{self.url}{endpoint}", **kwargs)
        if response.status_code != 200:
            raise Exception(response.text)
        
        if raw: 
            return response
        return response.json()
    
class EmoteSDK(BaseSDK, Singleton):
    def search(self, 
               query:      str       = None, 
               categories: List[str] = None, 
               tags:       List[str] = None, 
               authors:    List[str] = None,
               page:       int       = 1,
               limit:      int       = 9):
        
        params = dict(
            q = query,
            c = ','.join(categories) if categories else categories,
            t = ','.join(tags) if tags else tags,
            a = ','.join(authors) if authors else authors,
            p = page,
            l = limit
        )
        
        # clear empty values
        params = {k: v for k, v in params.items() if v}
        
        return self.call("GET", f"/search", params=params)

    def info(self):
        return self.call("GET", "/info")
    
    def get_categories(self):
        return self.call("GET", "/categories")
    
    def get_tags(self):
        return self.call("GET", "/tags")
    
    def get_authors(self):
        return self.call("GET", "/authors")

    def get_png(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/png", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp
    
    def get_gif(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/gif", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp

    def get_json(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/json", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp

    def upload(self, 
               path_json:  str,
               path_png:   str,
               path_gif:   str,
               categories: List[str],
               tags:       List[str]):
        
        upload_data = {}

        with open(path_json, "rb") as file:
            upload_data['json'] = base64.b64encode(file.read())
        
        with open(path_png, "rb") as file:
            upload_data['png'] = base64.b64encode(file.read())

        with open(path_gif, "rb") as file:
            upload_data['gif'] = base64.b64encode(file.read())
        
        with open(path_json, "r", encoding = 'utf-8') as file:
            data = json.load(file)
        
        upload_data.update({k: v for k, v in data.items() if k not in ('emote')})

        for key in ['isLoop', 'degrees', 'nsfw']:
            upload_data[key] = data['emote'].get(key, False)
        
        if upload_data['nsfw'] and not "NSFW" in categories:
            categories.append("NSFW")
        
        upload_data['tag'] = os.path.basename(path_json.replace('.json', ''))

        upload_data['categories'] = categories
        upload_data['tags'] = tags

        print({k: v for k, v in upload_data.items() if k not in ('json', 'png', 'gif')})

        return self.session.post(f"{self.url}/upload", json=upload_data).json()

    def _test(self, path_json:  str):

        with open(path_json, "rb") as file:
            jsn = base64.b64encode(file.read())

        return self.call("GET", "/test", json={"test": True, "пизда": "вагина"})

if __name__ == "__main__":
    emotes_sdk = EmoteSDK(api_key = os.environ.get('EMOTES_API_KEY'))
    #r = emotes_sdk._test()
    #path = os.path.expanduser('~') + '\\AppData\\Roaming\\.minecraft\\emotes\\'
    #name = "kiss"

    #from PIL import Image, ImageDraw, ImageFont #dynamic import

    #gif = f"{path}{name}.gif"
    #img = Image.open(gif)
    #img.save(name + ".png",'png', optimize=True, quality=70)

    #r = emotes_sdk.upload(
    #    f"{path}{name}.json", 
    #    f"{path}{name}.png", 
    #    f"{path}{name}.gif", 
    #    categories=["LOVE"], 
    #    tags=["KISS"])
    #print(r)
    #r = emotes_sdk.search(
    #    query="v5",
    #    authors=['BoBkiNN_']
    #)
    #r = emotes_sdk.get_json(
    #    "00101460-4644-b610-4430-d440084480c0"
    #)
    #print(r.json())