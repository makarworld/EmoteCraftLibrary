from functools import partial
import dearpygui.dearpygui as dpg
from dataclasses import dataclass
import os 
import json 
from PIL import Image
from threading import Thread

from textures import TEXTURES
from emotes_storage import local_emotes

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
            height=40
        )
    }

    pages = {
        'window': dict(
            label='Pages',
            height=40
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

def play_callback(sender, app_data, state):
    print('Play was clicked.')
    Thread(target=os.system, args=(f"python src/show_emote.py \"{state}\"",)).start()

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
            name = '.'.join(file.split('.')[:-1])

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
        self.ch_authors = []

        # pages
        self.pages = None
        self.pages_footer = None
        self.current_page = 1
        self.page_size = 30
        self.size_variants = [9, 30, 60, 90]
    
    def load_page(self):
        with dpg.group(horizontal=True):
            # categories window
            with dpg.child_window(**EmotesWindowSettings.categories['window']):
                
                dpg.add_text('Categories')
                categories = {
                    'Type': self.load_categories(),
                    'Tags': self.load_tags(),
                }

                for category, values in categories.items():
                    with dpg.tree_node(label=category, tag=f"{self.window_name}_{category}"):
                        for value in values:
                            dpg.add_checkbox(label=value)

                authors = set(self.load_authors())
                for author in authors:
                    it = dpg.add_checkbox(label=author, tag=f"{self.window_name}_{author}", parent=f"{self.window_name}_Author", callback=self.make_search)  
                    with dpg.tooltip(it):
                        dpg.add_text(author)
                    self.ch_authors.append(it)


            with dpg.group(horizontal=False):
                # search window
                with dpg.child_window(**EmotesWindowSettings.search['window']):
                    
                    with dpg.group(horizontal=True):
                        dpg.add_text('Search:')
                        dpg.add_input_text(default_value='', tag=f"{self.window_name}_search")
                        dpg.add_button(label='Sumbit', callback=self.make_search)

                # emotes list
                dpg.add_child_window(**EmotesWindowSettings.emotes_list['window'], tag=f"{self.window_name}_emotes_list_window")
                emotes = load_local_emotes()
                self.show_emotes(emotes[:self.page_size])


    def clear_emotes(self):
        dpg.delete_item(f"{self.window_name}_emotes_table")
        #dpg.delete_item(f"{self.window_name}_pages")
        dpg.delete_item(f"{self.window_name}_pages_footer")
        self.pages_footer = None


    def add_pages(self, parent: int, tag: str = ''):
        emotes = self.load_emotes()
        max_page = len(emotes) // self.page_size if len(emotes) % self.page_size == 0 else len(emotes) // self.page_size + 1
        with dpg.table(**EmotesWindowSettings.emotes_list['table'], parent=parent):
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            with dpg.table_row():
                with dpg.group(horizontal=True):
                    dpg.add_text('on page:')
                    dpg.add_combo(list(map(str, self.size_variants)), default_value=str(self.page_size), width=50, callback=self.onpage_change)


                with dpg.group(horizontal=True):
                    dpg.add_text(' ')
                    dpg.add_button(label='<<', callback=lambda: self.change_page(-2))

                    dpg.add_button(label='<', callback=lambda: self.change_page(-1))
                    dpg.add_text(f'{self.current_page} / {max_page}', tag=tag)
                    dpg.add_button(label='>', callback=lambda: self.change_page(+1))
                    dpg.add_button(label='>>', callback=lambda: self.change_page(+2))


                dpg.add_table_cell()

    def onpage_change(self, sender, app_data):
        self.page_size = int(dpg.get_value(sender))
        self.current_page = 1
        self.change_page(-2)

    def change_page(self, page: int):
        max_page = self.max_page()
        if (self.current_page == 1 and page == -1) or (self.current_page == max_page and page == +1):
            return

        self.clear_emotes()

        if page == +2:
            self.current_page = max_page

        elif page == -2:
            self.current_page = 1

        elif page in (+1, -1):
            self.current_page += page
        
        self.show_emotes(
            self.load_emotes(self.current_page, self.page_size)
        )
    

    
        dpg.configure_item(f"{self.window_name}_text_pages", default_value=f"{self.current_page} / {max_page}")
        dpg.configure_item(f"{self.window_name}_text_pages_footer", default_value=f"{self.current_page} / {max_page}")


    def load_emotes(self, page: int, size: int): ...
    
    def load_categories(self): ...
    
    def load_authors(self): ...

    def load_tags(self): ...
    
    def max_page(self): ...

    def show_emotes(self, emotes: list = None):

        if not self.pages:
            # show pages
            # page window 1
            self.pages = dpg.add_child_window(**EmotesWindowSettings.pages['window'], tag=f"{self.window_name}_pages", parent=f"{self.window_name}_emotes_list_window")
            self.add_pages(self.pages, tag=f"{self.window_name}_text_pages")

        emotes_count = 0
        #authors = []
        with dpg.table(
                    **EmotesWindowSettings.emotes_list['table'], 
                    tag=f"{self.window_name}_emotes_table", 
                    parent=f"{self.window_name}_emotes_list_window"):
            
            dpg.add_table_column()
            dpg.add_table_column()
            dpg.add_table_column()

            def create_emote_item(emotes_count):
                with dpg.child_window(**EmotesWindowSettings.emote['window']) as item: 

                    with dpg.group(horizontal=True):

                        with dpg.group(horizontal=False):
                            TEXTURES.paste_square_image(
                                "heart_off", size=EmotesWindowSettings.pin_size, user_data=(False), callback=like_callback)
                            
                            if emotes[emotes_count]['gif'] not in ('None', None):
                                TEXTURES.paste_square_image(
                                    "play", size=EmotesWindowSettings.pin_size, user_data=(emotes[emotes_count]['gif']), callback=play_callback)

                        for variant in ('image', 'gif'):
                            if emotes[emotes_count][variant] not in ('None', None):
                                try:
                                    TEXTURES.add(emotes[emotes_count][variant], tag = emotes[emotes_count]['tag'])

                                    TEXTURES.paste_square_image(
                                        emotes[emotes_count]['tag'], EmotesWindowSettings.emote['img_size'])
                                    break
                                except Exception as e:
                                    raise e
                                    continue
                        else:
                            TEXTURES.paste_square_image(
                                EmotesWindowSettings.emote['unknown'], EmotesWindowSettings.emote['img_size'])
                        
                        with dpg.group(horizontal=False):
                            it = TEXTURES.paste_square_image(
                                "list", size=EmotesWindowSettings.pin_size, user_data=(False), callback=like_callback)

                            TEXTURES.paste_square_image(
                                "download", size=EmotesWindowSettings.pin_size, user_data=(False), callback=like_callback)
                            
                    dpg.add_separator()

                    tooltip = (
                        f"Name: {emotes[emotes_count]['name']}\n\n"
                        f"Author: {emotes[emotes_count]['author']}\n\n"
                        f"Description: {emotes[emotes_count]['description']}"
                    )

                    MAX_LENGTH = 20
                    #item = dpg.add_text('[NSFW] [RUN]')
                    for col in ['name', 'author', 'description']: 
                        item = dpg.add_text(emotes[emotes_count][col] if len(emotes[emotes_count][col]) < MAX_LENGTH else emotes[emotes_count][col][:MAX_LENGTH].rstrip() + ' ...')
                        with dpg.tooltip(item):
                            dpg.add_text(tooltip)
                        #dpg.bind_item_font(item, ru_font)
                    #authors.append(emotes[emotes_count]['author'])
                    emotes_count += 1
                    return emotes_count


            for j in range(len(emotes) // 3):

                with dpg.table_row():

                    for i in range(3):
                        emotes_count = create_emote_item(emotes_count)
            else:
                if len(emotes) % 3 != 0:
                    with dpg.table_row():
                        for i in range(len(emotes) % 3):
                            emotes_count = create_emote_item(emotes_count)

        if not self.pages_footer:
            # show pages footer
            # page window 2
            self.pages_footer = dpg.add_child_window(**EmotesWindowSettings.pages['window'], tag=f"{self.window_name}_pages_footer", parent=f"{self.window_name}_emotes_list_window")
            self.add_pages(self.pages_footer, tag=f"{self.window_name}_text_pages_footer")


        #if not self.ch_authors:
        #    self.add_authors(authors)


    def make_search(self):
        #local_emotes.update_emotes()

        self.clear_emotes()

        authors = []

        for checkbox in self.ch_authors:
            if dpg.get_value(checkbox):
                label = dpg.get_item_label(checkbox)
                authors.append(label)
        
        emotes = []
        for author in authors:
            emotes += local_emotes.base.emotes.get(author=author)
        
        #print(emotes)

        self.show_emotes(emotes)



class LocalEmotes(EmotesWindow):

    def load_emotes(self, page: int, size: int):
        return load_local_emotes()
    
    def load_categories(self):
        return []
    
    def load_authors(self):
        return []

    def load_tags(self):
        return []
    
    def max_page(self):
        return len(self.load_emotes())

class FavoriteEmotes(EmotesWindow):

    def load_emotes(self, page: int, size: int):
        return load_local_emotes()
    
    def load_categories(self):
        return []
    
    def load_authors(self):
        return []

    def load_tags(self):
        return []
    
    def max_page(self):
        return len(self.load_emotes())

class OnlineEmotes(EmotesWindow):
    
    def load_emotes(self):
        return 

class OnlinePackEmotes(EmotesWindow):
    
    def load_emotes(self):
        return 

"""





"""