import dearpygui.dearpygui as dpg
from dataclasses import dataclass
import os 
import json 



from textures import TEXTURES

@dataclass
class EmotesWindowSettings:
    categories = {
        'window': dict(
            label='Categories', 
            width=175
        )
    }

    search = {
        'window': dict(
            label='Categories', 
            height=35
        )
    }

    emotes_list = {
        'window': dict(
            label='Emotes',
            border=False
        ),
        'table': dict(
            header_row=False, borders_innerH=False, 
            borders_outerH=False, borders_innerV=False, 
            borders_outerV=False)
    }

    emote = {
        'window': dict(
            label='Emote',
            height=195
        ),
        'img_size': 104,
        'unknown': 'bee5'
    }

    pin_size = 25

def like_callback(sender, app_data, state):
    print('Like was clicked.')
    dpg.set_item_user_data(sender, not state)
    #with sender:
        #with dpg.drawlist(width=25, height=25, callback=like_callback):
    if state is True:
        dpg.draw_image("heart_off", (0, 0), (25, 25), uv_min=(0, 0), uv_max=(1, 1), parent=sender)
    else:
        dpg.draw_image("heart_on", (0, 0), (25, 25), uv_min=(0, 0), uv_max=(1, 1), parent=sender)
    
    # reverse
    dpg.set_item_user_data(sender, not state)

def delete_colored_text(text: str):
    while "§" in text:
        i = text.find("§")
        text = text[:i] + text[i + 2:]
    return text

def load_local_emotes():
    path = dpg.get_value("minecraft_path")

    emotes = []

    if not os.path.exists(path + '/emotes'):
        raise
    

    for file in os.listdir(path + '/emotes'):
        if file.endswith('.json'):
            name = file.split('.')[0]

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
            
            emotes.append({
                'image': image,
                'gif': gif,
                'tag': name,
                'name': delete_colored_text(data["name"]),
                'author': delete_colored_text(data["author"]),
                'description': delete_colored_text(data["description"])
            })
    
    return emotes



class EmotesWindow:
    def __init__(self, window_name: str):
        self.window_name = window_name
    
    def load_page(self):
        with dpg.group(horizontal=True):
            # categories window
            with dpg.child_window(**EmotesWindowSettings.categories['window']):
                
                dpg.add_text('Categories')
                categories = {
                    'Type': ['ANY', 'DANCE', 'POSE', 'RUN', 'ITEM CONTROL', 'NSFW'],
                    'Tags': ['SEX', 'FLY', 'INVISIBLE'],
                    'Author': []
                }

                for category, values in categories.items():
                    with dpg.tree_node(label=category, tag=f"{self.window_name}_{category}"):
                        for value in values:
                            dpg.add_checkbox(label=value)


            with dpg.group(horizontal=False):
                # search window
                with dpg.child_window(**EmotesWindowSettings.search['window']):
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text('Search:')
                        dpg.add_input_text(default_value='', tag=f"{self.window_name}_search")
                        dpg.add_button(label='Sumbit', callback=self.make_search)
                
                # emotes list
                dpg.add_child_window(**EmotesWindowSettings.emotes_list['window'], tag=f"{self.window_name}_emotes_list_window")
                self.show_emotes()
                    

    def load_emotes(self):
        pass

    def show_emotes(self):
        emotes = load_local_emotes()

        emotes_count = 0
        authors = []
        with dpg.table(
                    **EmotesWindowSettings.emotes_list['table'], 
                    tag=f"{self.window_name}_emotes_table", 
                    parent=f"{self.window_name}_emotes_list_window"):
            
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            for j in range(len(emotes) // 3):

                with dpg.table_row():

                    for i in range(3):

                        with dpg.child_window(**EmotesWindowSettings.emote['window']) as item: 

                            with dpg.group(horizontal=True):

                                #with dpg.group(horizontal=False):
                                #with dpg.drawlist(width=25, height=25, user_data=(False), callback=like_callback):
                                #    dpg.draw_image("heart_off", (0, 0), (25, 25), uv_min=(0, 0), uv_max=(1, 1))

                                TEXTURES.paste_square_image(
                                    "heart_off", size=EmotesWindowSettings.pin_size, user_data=(False), callback=like_callback)

                                        

                                    #it = dpg.add_image_button(texture_tag="heart_off", tag=f"like_{i}{j}", width=25, height=25, background_color=(37,37,38))
                                    #dpg.bind_item_theme(it, orng_btn_theme)
                                
                                if emotes[emotes_count]['image'] is not None:
                                    try:
                                        TEXTURES.add(emotes[emotes_count]['image'], tag = emotes[emotes_count]['tag'])

                                        TEXTURES.paste_square_image(
                                            emotes[emotes_count]['tag'], EmotesWindowSettings.emote['img_size'], user_data=(False), callback=like_callback)

                                    except: 
                                        TEXTURES.paste_square_image(
                                            EmotesWindowSettings.emote['unknown'], EmotesWindowSettings.emote['img_size'], user_data=(False), callback=like_callback)
                                else:
                                    TEXTURES.paste_square_image(
                                        EmotesWindowSettings.emote['unknown'], EmotesWindowSettings.emote['img_size'], user_data=(False), callback=like_callback)
                                    
                                TEXTURES.paste_square_image(
                                    "list", size=EmotesWindowSettings.pin_size, user_data=(False), callback=like_callback)
                                
                            dpg.add_separator()

                            tooltip = (
                                f"Name: {emotes[emotes_count]['name']}\n\n"
                                f"Author: {emotes[emotes_count]['author']}\n\n"
                                f"Description: {emotes[emotes_count]['description']}"
                            )

                            MAX_LENGTH = 20

                            for col in ['name', 'author', 'description']:
                                item = dpg.add_text(emotes[emotes_count][col] if len(emotes[emotes_count][col]) < MAX_LENGTH else emotes[emotes_count][col][:MAX_LENGTH].rstrip() + ' ...')
                                with dpg.tooltip(item):
                                    dpg.add_text(tooltip)
                                #dpg.bind_item_font(item, ru_font)
                            authors.append(emotes[emotes_count]['author'])
                            emotes_count += 1

        authors = set(authors)
        for author in authors:
            it = dpg.add_checkbox(label=author, parent=f"{self.window_name}_Author")  
            with dpg.tooltip(it):
                dpg.add_text(author)


    def make_search(self):
        dpg.delete_item(f"{self.window_name}_emotes_table")


"""





"""