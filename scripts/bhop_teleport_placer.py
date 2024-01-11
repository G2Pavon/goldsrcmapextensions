# bhop_teleport_placer.py
"""
Automatic teleport placer for bhop stages.
https://github.com/G2Pavon/goldsrcmapextensions/blob/main/bhop_teleport_placer.md

When use:

1. The start is at same height as the end of the stage:

start                     end        
=====                   ========
    |                   |                    
    |___________________|                

2. The start is higher than end of the stage:

start                      
=====                 
    |                       end             
    |                     =======
    |_____________________|       

    
3. The start is lower than end of the stage and the teleport floor is flat:

                    end
                  ======
start             |        
=====             |   
    |_____________|


When NOT use:

NOT use when the start is lower than teleport floor:

                          end
                       =======
start           _______|
======         /
     |        /
     |_______/


TODO:
- Auto-set the destination angle: Currently not implemented. Consider using the vector from trigger.origin to destination.origin to get an approximate angle.
- Change teleport thickness
"""
import goldsrcmap as gsm

INPUT = '/path/to/your.map'
OUTPUT = '/path/to/your.map'
DESTINATION_HEIGHT = 64  #Change it according to your needs
TP_FLOOR_HEIGHT = 16 #Change it according to your needs
CUSTOM_ENTITY = 'kz_bhop_stage' # You can use a custom classname

m = gsm.load_map(INPUT)

i = 0  # bhop stage counter
for entity in m:
    if entity == CUSTOM_ENTITY:
        i += 1
        # For check the lower and higher brush
        min_z = min(vertex.z for brush in entity for vertex in brush.vertices)
        max_z = max(vertex.z for brush in entity for vertex in brush.vertices)

        destination = gsm.Entity()
        teleport = gsm.Entity()

        for brush in entity:
            for vertex in brush.vertices:
                # Check for the lowest Z coordinate to place trigger
                if min_z == vertex.z:
                    trigger = brush.copy()
                    trigger.move_by(0, 0, TP_FLOOR_HEIGHT)
                    trigger.set_texture('aaatrigger')

                    teleport.properties = {
                        "classname": "trigger_teleport",
                        "target": f"tele{i}"
                    }

                # Check for the highest Z coordinate to place destination
                if max_z == vertex.z:
                    destination.properties = {
                        "classname": "info_teleport_destination",
                        "targetname": f"tele{i}",
                        "origin": f"{brush.origin.x} {brush.origin.y} {brush.origin.z + DESTINATION_HEIGHT}" 
                    }

        # Add trigger and destination to map
        teleport.add_brush(trigger)
        m.add_entity(teleport, destination)

        # Add kz_bhop_stage brushes to worldspawn (convert to world)
        m.add_brush(entity.brushes)

        # "Delete" kz_bhop_stage entity
        entity.properties = {}
        entity.brushes = []

gsm.save_map(m, OUTPUT)
