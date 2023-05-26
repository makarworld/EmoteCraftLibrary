
import glob
from PIL import Image
import sys 

def make_gif(frame_folder, output):
    pngs = [Image.open(image) for image in glob.glob(f"{frame_folder}/*.png")]

    frames = [[tmp := Image.new('RGBA', image.size, (255,255,255,255)), tmp.paste(image, (0,0), image), tmp][-1] for image in pngs]

    frame_one: Image = frames[0]
    frame_one.save(f"{output}.gif", format="GIF", append_images=frames,
               save_all=True, duration=len(frames) // 10, loop=0)
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 create_gif.py <output>")
        exit(1)

    output = sys.argv[1]
    make_gif("./render", output)