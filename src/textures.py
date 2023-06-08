import os
import dearpygui.dearpygui as dpg
import random
import shutil

class TexturesManager:
    def __init__(self):
        self.tags = {} 
    
    def load_folder(self, path: str) -> list:
        accepted = (
            ".png", ".jpg", ".jpeg", ".bmp", 
            ".psd", ".gif", ".hdr", ".pic", 
            ".ppm", ".pgm")
        
        files = [file for file in os.listdir(path) if file.endswith(accepted)]
        return [
            self.add(os.path.join(path, file), file.split(".")[0]) 
            for file in files
        ]

    def random_name(self) -> str:
        string = 'abcdefghijklmnopqrstuvwxyz0123456789'
        return ''.join(random.choices(string, k=16))

    def add(self, filename: str, tag: str, show=False) -> str:
        if self.tags.get(tag):
            return tag
        
        # check is unicode chars in name
        if not filename.isascii() or " " in filename:
            name = self.random_name() + '.' + filename.split(".")[-1]
            shutil.copyfile(filename, name)
        
            width, height, channels, data = dpg.load_image(name)
            os.remove(name)
        else:
            width, height, channels, data = dpg.load_image(filename)

        with dpg.texture_registry(show=show):
            dpg.add_static_texture(
                width=width, height=height, 
                default_value=data, tag=tag)
        
            self.tags[tag] = filename

        return tag

    def add_content(self, content: bytes, width: int, height: int, tag: str, show=False) -> str:
        if self.tags.get(tag):
            return tag
        
        with dpg.texture_registry(show=show):
            dpg.add_static_texture(
                width=width, height=height, 
                default_value=content, tag=tag)
        
            self.tags[tag] = "binary"

        return tag

    def paste_image(
                self,
                texture_tag: str, 
                main_width: int = 100, main_height: int = 100,
                user_data = None, callback = None,
                pmin= (0, 0), pmax= (100, 100),
                uv_min=(0, 0), uv_max=(1, 1)
                ):
    
        with dpg.drawlist(width=main_width, height=main_height, user_data=user_data, callback=callback) as drawlist:
            drawimage = dpg.draw_image(texture_tag, pmin=pmin, pmax=pmax, uv_min=uv_min, uv_max=uv_max)
        return drawimage
    
    def paste_square_image(
                self,
                texture_tag: str,
                size: int = 100,
                user_data = None, callback = None
                ):

        return self.paste_image(
            texture_tag, main_width=size, main_height=size, user_data=user_data, callback=callback,
            pmax = (size, size),
        )
TEXTURES = TexturesManager()

if __name__ == "__main__":
    dpg.create_context()
    dpg.create_viewport(title='Custom Title', width=800, height=600)

    TEXTURES.load_folder("./src/textures")

    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
