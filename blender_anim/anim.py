
import logging
from random import uniform
import math

import bpy


#def update_scene(scene):
#    if scene.frame_current == 30:
#        bpy.ops.screen.animation_cancel(restore_frame=False)

bpy.context.scene.render.resolution_x = 800
bpy.context.scene.render.resolution_y = 800



camera = bpy.data.objects["Camera"]
#print(camera.location)
#input()

if __name__ == "__main__":
    #bpy.app.handlers.frame_change_pre.append(update_scene)
    bpy.ops.screen.animation_play()