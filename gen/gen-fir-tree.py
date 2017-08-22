'''
Emily Donahue, 2016
Blender script to generate a pine bough

Update 2017-08-21: re-named from 'gen-pine-tree.py' to specify that this script 
  will generate a fir-type tree
  
  TODO: figure out how to make cones more 'pinched'
'''

import bpy
import bmesh
import mathutils
import math
import random

# custom module imports
import os, sys

file_path = os.getcwd() # if started from icon, cwd = ~
scripts_path = os.path.join(file_path, 'blender/scripts')
utils_path = os.path.join(scripts_path, 'utils')

if utils_path not in sys.path:
    sys.path.append(utils_path)

from blendutils import *

scene = bpy.context.scene
            

def create_cone(scale=1.0):

    bpy.ops.mesh.primitive_cone_add(
        vertices = 12,
        location = ((0, 0, 0)),
        enter_editmode=True
    )
    
    bpy.ops.transform.resize(
        value = (scale, scale, scale)
    )

    # triangulate, then subdivide
    bpy.ops.mesh.quads_convert_to_tris(use_beauty=False)
    bpy.ops.mesh.subdivide(smoothness=0)
    
    # cast to sphere
    object_mode()
    bpy.ops.object.modifier_add(type='CAST')
    bpy.context.object.modifiers["Cast"].use_x = False
    bpy.context.object.modifiers["Cast"].use_y = False
    bpy.context.object.modifiers["Cast"].factor = 1.0
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Cast")
    
    # random displacement
    rand_tex = bpy.data.textures.new('rand_tex', type='NOISE')
    activ_obj = bpy.context.active_object
    displ_mod = activ_obj.modifiers.new("rand_disp", type='DISPLACE')
    displ_mod.texture = rand_tex
    displ_mod.mid_level = 0.5
    displ_mod.strength = 0.1
    bpy.ops.object.modifier_apply(apply_as='DATA', 
                                  modifier="rand_disp")
    
    select_none()

if __name__=='__main__':
    
    object_mode()
    delete_everything()
    
    scales = [1.0, 2.0, 3.0]
    
    last_scale = 0.0
    for scale in scales:
        create_cone(scale=scale)
        select_all()
        # delta_z = (last_scale + scale) / 2
        delta_z = scale / 2  
        last_scale = scale              
        bpy.ops.transform.translate(value=(0, 0, delta_z))
      
    
