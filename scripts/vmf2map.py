import argparse
import os
import goldsrcmap as gsm

TOOLS_TEXTURES = {
    "toolsnodraw": "null",
    "toolstrigger": "aaatrigger",
    "toolsskybox": "sky",
    "toolsskip": "skip",
    "toolshint": "hint",
    "toolsplayerclip": "clip",
    "toolsorigin": "origin",
    "toolsblack": "black"
}

ENTITY_CONVERT = {
    "info_player_counterterrorist": "info_player_start",
    "info_player_terrorist": "info_player_deathmatch"
}

def convert_vmf_to_map(input_vmf, output_map):
    brace_count = 0 
    vmf_name = os.path.splitext(os.path.basename(input_vmf))[0]
    map_obj = gsm.Map(vmf_name)

    current_entity = None
    current_brush = None
    current_face = None

    is_entity = False
    is_brush = False
    is_side = False

    with open(input_vmf,'r') as vmf:
        for line in vmf.readlines():

            # Skip comments
            if line.startswith('//'):
                continue
            
            elif line.strip() == "world" or line.strip() == "entity":
                is_entity = True
            elif line.strip() == "solid":
                is_brush = True
            elif line.strip() == "side":
                is_side = True

            elif line.strip().startswith("{"):
                brace_count += 1
                if brace_count == 1 and is_entity:
                    current_entity = gsm.Entity()

                elif brace_count == 2 and is_brush:
                    current_brush = gsm.Brush()

            elif line.strip().startswith("}"):
                brace_count -= 1
                if brace_count == 1:
                    if is_brush:
                        current_entity.add_brush(current_brush)
                        is_brush = False
                elif brace_count == 2:
                    if is_side:
                        texture = gsm.Texture(texture_name, u_axis, u_offset, v_axis, v_offset, 0, u_scale, v_scale)
                        current_face = gsm.Face(plane, texture)
                        current_brush.add_face(current_face)
                        is_side = False

                elif brace_count == 0:
                    if is_entity:
                        map_obj.add_entity(current_entity)
                        is_entity = False
                

            # Entity properties
            elif brace_count == 1 and line.strip().startswith('"'):
                if is_entity:
                    k, v = line.strip().split('" "', 1)
                    key, value = k.replace('"', ''), v.replace('"', '')
                    if value in ENTITY_CONVERT:
                        value = ENTITY_CONVERT[value]
                    current_entity.properties[key] = value

            # Brush face properties
            elif brace_count == 3 and line.strip().startswith('"'):
                if is_side:
                    k, v = line.strip().split('" "', 1)
                    key, value = k.replace('"', ''), v.replace('"', '')
                    if key == "plane":
                        plane_info = value.split(' ')
                        plane = gsm.Plane(
                            gsm.Point(float(plane_info[0].strip('(')), float(plane_info[1]), float(plane_info[2].strip(')'))),
                            gsm.Point(float(plane_info[3].strip('(')), float(plane_info[4]), float(plane_info[5].strip(')'))),
                            gsm.Point(float(plane_info[6].strip('(')), float(plane_info[7]), float(plane_info[8].strip(')')))
                        )

                    elif key == "material":
                        texture_name = value.split('/')[-1]
                        texture_name = texture_name.split(' ')[0]
                        if texture_name in TOOLS_TEXTURES:
                            texture_name = TOOLS_TEXTURES[texture_name]

                    elif key == "uaxis":
                        uaxis_info = value.split()
                        u_axis = gsm.Vector3(float(uaxis_info[0].strip('[')), float(uaxis_info[1]), float(uaxis_info[2]))
                        u_offset = float(uaxis_info[3].strip(']'))
                        u_scale = float(uaxis_info[4])
                    
                    elif key == "vaxis":
                        vaxis_info = value.split()
                        v_axis = gsm.Vector3(float(vaxis_info[0].strip('[')), float(vaxis_info[1]), float(vaxis_info[2]))
                        v_offset = float(vaxis_info[3].strip(']'))
                        v_scale = float(vaxis_info[4])


    # Adding wad property
    map_obj.worldspawn["wad"] = ""

    gsm.save_map(map_obj, output_map)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Convert VMF file to MAP file")
    parser.add_argument("input_vmf", type=str, help="Input VMF file path")
    parser.add_argument("output_map", type=str, help="Output MAP file path")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    input_vmf = args.input_vmf
    output_map = args.output_map

    convert_vmf_to_map(input_vmf, output_map)