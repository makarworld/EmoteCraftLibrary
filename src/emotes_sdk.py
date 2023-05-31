from typing import List
import requests

class BaseSDK:
    def __init__(self, api_key: str = None, test: bool = True):
        self.api_key = api_key
        self.test = test

        #if self.test:
        self.url = "http://127.0.0.1:5000/"

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

    def get_png(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/png", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp.content
    
    def get_gif(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/gif", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp.content

    def get_json(self, uuid: str, path_to_save: str = None):
        resp = self.call("GET", f"/emote/{uuid}/json", raw = True)
        if path_to_save:
            with open(path_to_save, 'wb') as f:
                f.write(resp.content)
        return resp.content

if __name__ == "__main__":
    emotes_sdk = BaseSDK()
    #resp = emotes_sdk.search(
    #    #query="test",
    #    categories=["RUN", "SEX"],
    #    #tags=["test"],
    #    #authors=["test"],
    #    page=1,
    #    limit=9
    #)
    #print(resp.json())
    emotes_sdk.get_png(123, "test.png")