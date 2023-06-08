from __future__ import annotations
from dataclasses import dataclass
import json
import os
import dearpygui.dearpygui as dpg


from emotes_window import LocalEmotes, FavoriteEmotes, OnlineEmotes, OnlinePackEmotes
from emotes_storage import local_emotes

SIZE = (800, 834)

dpg.create_context()
dpg.create_viewport(title='EmoteCraft - Emotes Library', width=SIZE[0], height=SIZE[1], min_width=SIZE[0], min_height=SIZE[1])
dpg.setup_dearpygui()
#dpg.show_debug()

# add a font registry
with dpg.font_registry():

    with dpg.font("./src/fonts/notomono-regular.ttf", 13, default_font=True, tag="Default font") as f:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)
        dpg.add_char_remap([0x00E0, 0x00E4],[0x0430,0x0434])
    
dpg.bind_font("Default font")

window = dict(
    label='EmoteCraft - Emotes Library',
    tag='primary',
    no_close=True,
    no_move=True,
    no_title_bar=True,
    menubar=True
)

@dataclass
class MainWindow:
    minecraft_path = {
        'window': dict(
            label = 'Minecraft folder selection', 
            height=75,
        ),
        'default_path': os.path.expanduser('~') + '\\AppData\\Roaming\\.minecraft'
    }

    tabs = {
        'window': dict(
                label = 'Emotes',
                border=False
        )
    }

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
            borders_outerV=False, tag="emotes_table")
    }

    emote = {
        'window': dict(
            label='Emote',
            height=195
        ),
        'img_size': 104
    }

    pin_size = 25

# load all textures
from textures import TEXTURES
TEXTURES.load_folder("./src/textures")


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

def make_search(): 
    dpg.delete_item("emotes_table")



def main_window():

    # main window
    with dpg.window(**window):

        #menubar
        with dpg.menu_bar():
            dpg.add_menu_item(label='Settings')


        # Minecraft folder selection window
        with dpg.child_window(**MainWindow.minecraft_path['window']):
            
            # <===- Browse folder button -===>

            # Callback on success selected item
            def callback(sender, app_data, user_data):

                if os.path.exists(app_data['file_path_name'] + '/emotes'):
                    dpg.set_value('minecraft_path', app_data['file_path_name'])
                    #load_local_emotes()
                else:
                    pass # show error

            # Callback on cancel
            def cancel_callback(sender, app_data):
                print('Cancel was clicked.')
                print("Sender: ", sender)
                print("App Data: ", app_data)


            # <===- END Browse folder button -===>

            # <===- Minecraft folder selection window -===>
            dpg.add_text('Minecraft PATH:')
            with dpg.group(horizontal=True):
                dpg.add_input_text(default_value=MainWindow.minecraft_path['default_path'], tag='minecraft_path')

                # Browse file dialog
                dpg.add_file_dialog(
                    directory_selector=True, show=False, callback=callback, tag="file_dialog_id",
                    cancel_callback=cancel_callback, width=700 ,height=400, default_path=MainWindow.minecraft_path['default_path'])
                
                dpg.add_button(label='Browse', callback=lambda: dpg.show_item("file_dialog_id"))

            # <===- END Minecraft folder selection window -===>

        
        with dpg.child_window(**MainWindow.tabs['window']):
            with dpg.tab_bar():
                
                with dpg.tab(label="My emotes", tag="my_emotes"):

                    my_emotes = LocalEmotes('my_emotes')
                    #my_emotes.load_page()                                 


                with dpg.tab(label="Favorites", tag="favorites_tab"):
                    favorites = FavoriteEmotes('favorites')
                    #favorites.load_page()  

                with dpg.tab(label="Search", tag="search_tab"):
                    search_emotes = OnlineEmotes('search_emotes')
                    search_emotes.load_page()  

                with dpg.tab(label="Packs", tag="packs_tab"):
                    packs_emotes = OnlinePackEmotes('packs_emotes')
                    #packs_emotes.load_page()          

if __name__ == '__main__':
    # show main window
    main_window()

    dpg.show_viewport()

    dpg.set_primary_window(window['tag'], True)

    dpg.start_dearpygui()
    dpg.destroy_context()