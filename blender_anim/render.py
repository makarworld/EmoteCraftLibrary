import json
import os 
import shutil
import json
import os             
import math


def main(emote):
    config = {
        "emote_path": f'{os.path.expanduser("~")}\\AppData\\Roaming\\.minecraft\\emotes\\{emote}.json'
    }

    # save config
    with open('./render.json', 'w') as f:
        json.dump(config, f, indent=4)




    if not os.path.exists('./anim.blend_clear'):
        raise

    if os.path.exists('./anim.blend'):
        os.remove('./anim.blend')


    shutil.copy("anim.blend_clear", "anim.blend")

    # clear render folder
    for f in os.listdir('render'):
        os.remove(os.path.join('render', f))

    # import emote to blender
    os.system("blender -b anim.blend --python bimport.py")

    # start render
    os.system("blender -b anim.blend --render-output //render/emote_######.png -a")

    # create gif
    os.system(f"python create_gif.py \"{emote}\"")

if __name__ == "__main__":
    all_files = os.listdir(f'{os.path.expanduser("~")}\\AppData\\Roaming\\.minecraft\\emotes')
    emotes = [x.replace('.json', '') for x in all_files if x.endswith(".json")]
    for emote in emotes:

        if f'{emote}.gif' not in all_files:
            print(f'{emote}.gif not found')
            #input()
            main(emote)
            shutil.copyfile(f'{emote}.gif', f'{os.path.expanduser("~")}\\AppData\\Roaming\\.minecraft\\emotes\\{emote}.gif')
            os.remove(f'{emote}.gif')
    else:
        print('All emotes were rendered.')