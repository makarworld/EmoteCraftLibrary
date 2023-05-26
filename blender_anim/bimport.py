import bpy
import json

# Thanks ЗАРАЗЕН

def import_to_blender(emote_path):
    with open(emote_path, "r", encoding="utf-8") as f:
        emote_data = json.load(f)

    data = emote_data["emote"]
    bpy.context.scene.frame_start = data["returnTick"]
    bpy.context.scene.frame_end = data["endTick"]

    for i in data["moves"]:
        
        
        bpy.context.scene.frame_set(i["tick"])
        
        name = list(i.keys())[3]

        bpy.data.objects[name].select_set(True)
        
        
        
        typ = list(i[name].keys())[0]
        value = i[name][typ]
        
        
        if (name == "rightItem" or name == "leftItem"):
            if (typ == "z"):
                typ = "y"
            elif (typ == "y"):
                typ = "z"
                
        if (name == "rightItem" or name == "leftItem"):
            if (typ == "roll"):
                typ = "yaw"
            elif (typ == "yaw"):
                typ = "roll"
        
        
        if(name == 'rightArm' or name == 'leftArm'):
            if typ == 'y':
                value -= 12
        
        if(typ == 'z' or typ == 'x'):
            if(name == "rightLeg"):
                value -= 0.1
            elif(name == "leftLeg"):
                value += 0.1
        
        if(typ == 'y'):
            if(name == "rightLeg" or name == "leftLeg"):
                value -= 12
        
        elif (name != "rightItem" and name != "leftItem"):
            pass
        elif(not (name == 'torso' and not (typ == 'roll' or typ == 'bend'))): # rotation correction (*-1) except for torzo roll/bend
            value = value * -1
        
        if(typ == "x" or typ == "y" or typ == "z"):
            if(not name == 'torso'):
                value = value / 4
                if (name != "rightItem" and name != "leftItem"):
                    value = value * -1
            else:
                value = value / 0.25
                if(typ == 'z'):
                    value = value * -1
        
        if(name == 'head' and typ == 'y'):
            value += 3
        
        
        
        
        if (name == "rightItem" or name == "leftItem"):
            if(typ == "z" or typ == "x"):
                value = value * -1
        
        
        if (name == "torso" and (typ == "pitch" or typ == "yaw")):
            value = value * -1
        

        
        
        if typ == "pitch":
            bpy.data.objects[name].rotation_euler[0] = -value
            bpy.data.objects[name].keyframe_insert(data_path = "rotation_euler")
            
        elif typ == "yaw":
            bpy.data.objects[name].rotation_euler[2] = -value
            bpy.data.objects[name].keyframe_insert(data_path = "rotation_euler")
            
        elif typ == "roll":
            bpy.data.objects[name].rotation_euler[1] = -value
            bpy.data.objects[name].keyframe_insert(data_path = "rotation_euler")
            
        elif typ == "x":
            bpy.data.objects[name].location[0] = value
            bpy.data.objects[name].keyframe_insert(data_path = "location")
            
        elif typ == "y":
            bpy.data.objects[name].location[2] = value
            bpy.data.objects[name].keyframe_insert(data_path = "location")
            
        elif typ == "z":
            bpy.data.objects[name].location[1] = value
            bpy.data.objects[name].keyframe_insert(data_path = "location")
            
        elif typ == "bend":
            bpy.data.objects[name + "_bend"].rotation_euler[0] = -value
            bpy.data.objects[name + "_bend"].keyframe_insert(data_path = "rotation_euler")
            
        
        
        bpy.data.objects[name].select_set(False)

    bpy.ops.wm.save_mainfile()

def load_render_cfg():
    with open("render.json", "r", encoding="utf-8") as f:
        return json.load(f)

if __name__ == "__main__":
    config = load_render_cfg()
    import_to_blender(emote_path = config["emote_path"])