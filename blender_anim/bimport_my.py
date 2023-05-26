import bpy
import json
import os             
import math


def import_to_blender(emote_path):
    #emote_path = os.path.expanduser('~') + '\\AppData\\Roaming\\.minecraft\\emotes\\SPE_Dance of little chickens.json'
    # Load the JSON file
    with open(emote_path, "r", encoding="utf-8") as f:
        emote_data = json.load(f)


    def reverse_getPartData(emote_data):
        inserted = 0
        for movement in emote_data['emote']['moves']:
            for bone_name, bone_data in movement.items():
                if bone_name in ["tick", "easing", "turn"]:
                    continue
                # clear
                # bpy.data.objects[bone_name].animation_data_clear()
                # continue 
            
                fcurves = bpy.data.objects[bone_name].animation_data.action.fcurves
                typ = list(bone_data.keys())[0]

                if typ == 'x':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'location' and fcurve.array_index == 0)][0]
                    isLocation = True

                elif typ == 'z':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'location' and fcurve.array_index == 1)][0]
                    isLocation = True

                elif typ == 'y':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'location' and fcurve.array_index == 2)][0]
                    isLocation = True


                elif typ == 'pitch':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'rotation_euler' and fcurve.array_index == 0)][0]
                    isLocation = False

                elif typ == 'roll':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'rotation_euler' and fcurve.array_index == 1)][0]
                    isLocation = False

                elif typ == 'yaw':
                    fcurve = [fcurve for fcurve in fcurves if (
                        fcurve.data_path == 'rotation_euler' and fcurve.array_index == 2)][0]
                    isLocation = False

                if typ != 'bend':
                    # add keyframe
                    print(movement)
                    easing, interpolation, value = reverse_getTickData(movement['easing'], bone_name, typ, movement[bone_name][typ], isLocation)
                    print(easing, interpolation, value)
                    
                    #if typ in ["pitch", "yaw", "roll", "bend"]:
                        #value = value * -1
                    
                    keyframe = fcurve.keyframe_points.insert(movement['tick'], value)
                    print(keyframe)
                    print(keyframe.easing)
                    print(keyframe.interpolation)
                    
                    keyframe.easing = easing
                    keyframe.interpolation = interpolation
                    
                    print(keyframe)
                    print(keyframe.easing)
                    print(keyframe.interpolation)
                    inserted += 1
                else:
                    # typ == "bend"
                    
                    if bone_name == "head":
                        continue
                    
                    bend_name = bone_name + "_bend"
                    
                    fcurve = [fcurve for fcurve in bpy.data.objects[bend_name].animation_data.action.fcurves if (
                        fcurve.data_path == 'rotation_euler' and fcurve.array_index == 0)][0]
                        
                    # add keyframe
                    print(movement)
                    reversed_data = reverse_getTickData(movement['easing'], bone_name, typ, movement[bone_name][typ], False)
                    print(reversed_data)

                    keyframe = fcurve.keyframe_points.insert(movement['tick'], reversed_data[2])
                    print(keyframe)
                    print(keyframe.easing)
                    print(keyframe.interpolation)
                    
                    keyframe.easing = reversed_data[0]
                    keyframe.interpolation = reversed_data[1]
                    
                    print(keyframe)
                    print(keyframe.easing)
                    print(keyframe.interpolation)
                    inserted += 1
                
        print(f"total moves: {len(emote_data['emote']['moves'])}")  
        print(f"inserted moves: {inserted}") 
        
    def reverse_getTickData(easing, name, typ, value, isL):

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

        if(isL):
            if(not name == 'torso'):
                value = abs(value * 0.25)
            else:
                value = value * 4
                if(typ == 'z'):
                    value = abs(value)

        elif(not (name == 'torso' and not (typ == 'roll' or typ == 'bend'))):
            value = abs(value)

        if(name == 'head' and typ == 'y'):
            value += 3

        if easing.endswith("QUAD"):
            interpolation = "BEZIER"
            easing = easing.replace("QUAD", "")

        if easing.endswith("CONSTANT"):
            interpolation = "CONSTANT"
            easing = easing.replace("CONSTANT", "")
        
        if easing.endswith("LINEAR"):
            interpolation = "LINEAR"
            easing = easing.replace("LINEAR", "")


        if easing == "EASEINOUT":
            keasing = "AUTO"
        else:
            keasing = '_'.join(list(easing))
        
        return keasing, interpolation, value

    reverse_getPartData(emote_data)

    #additional info
    bpy.context.scene.frame_start = emote_data["emote"]["beginTick"]
    bpy.context.scene.frame_end = emote_data["emote"]["endTick"]

    bpy.ops.wm.save_mainfile()