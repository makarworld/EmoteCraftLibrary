"""Local storage for your emotes"""
import dearpygui.dearpygui as dpg
from mwsqlite import MWBase
import os
import json
import hashlib

def delete_colored_text(text: str):
    while "§" in text:
        i = text.find("§")
        text = text[:i] + text[i + 2:]
    return text

class EmotesStorage:
    def __init__(self):
        self.base = MWBase('localemotes.db', {
            'emotes': {
                'name': str,
                'author': str,
                'description': str,
                'uuid': str,
                'tag': str,
                'path': str,
                'image': str,
                'gif': str,
                'favorite': bool,
                'nsfw': bool
            }
        })
    
    def generate_uuid(self, data):
        """
        Emote UUID generator by name, author, description.
        """
        # f50ec0b7-f960-400d-91f0-c42a6d44e3d0
        #
        string = '0123456789abcdef'
        unic = data['name'].lower() + data['author'].lower() + data['description'].lower()
        unic = unic.replace(' ', '')
        uuid = sum([ord(x) for x in hashlib.md5(unic.encode()).hexdigest()])
        bighash = 89809223 + uuid
        uuid = ''.join([string[x] if x < len(string) else string[x - 16] for x in [bighash % i for i in range(1, 33)]])
        uuid = f"{uuid[:8]}-{uuid[8:12]}-{uuid[12:16]}-{uuid[16:20]}-{uuid[20:]}"

        return uuid
        

        


    def update_emotes(self):
        path = dpg.get_value("minecraft_path")

        emotes = []

        if not os.path.exists(path + '/emotes'):
            raise
        

        for file in os.listdir(path + '/emotes'):
            if file.endswith('.json'):
                name = '.'.join(file.split('.')[:-1])
                if self.base.emotes.get_one(name=name):
                    continue
                
                file_path = os.path.join(path, f'emotes/{name}.json')

                if os.path.exists(f'{path}/emotes/{name}.png'):
                    image = os.path.join(path, f'emotes/{name}.png')
                else:
                    image = None

                if os.path.exists(f'{path}/emotes/{name}.gif'):
                    gif = os.path.join(path, f'emotes/{name}.gif')
                else:
                    gif = None
                
                with open(path + '/emotes/' + file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # if uuid already exists in database -> skip
                print(data)
                print(self.generate_uuid(data))
                if self.base.emotes.get(uuid=data.get("uuid", self.generate_uuid(data))):
                    continue

                emote_data = dict(
                    name        = delete_colored_text(data["name"]),
                    author      = delete_colored_text(data["author"]),
                    description = delete_colored_text(data["description"]),
                    uuid        = data.get("uuid", self.generate_uuid(data)),
                    tag         = name,
                    path        = file_path,
                    image       = image,
                    gif         = gif,
                    favorite    = False,
                    nsfw        = data["emote"].get("nsfw", False)
                )

                self.base.emotes.add(**emote_data)

                emotes.append(emote_data)
        
        return emotes

    def call(self, method: str, *args, **kwargs):
        return self.base.emotes.__getattr__(method)(*args, **kwargs)


    
local_emotes = EmotesStorage()
#local_emotes.update_emotes()