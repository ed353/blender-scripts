'''
Emily Donahue, 2016
Blender script to generate a pine bough

Update 2017-08-21: re-named from 'gen-pine-tree.py' to specify that this script 
  will generate a fir-type tree
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
            
def start_tree(scale=1.0):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1,
        vertices=10,
        location=(0,0,1),
        enter_editmode=True
    )      
    
    bpy.ops.transform.resize(
        value = (scale, scale, scale)
    )
  
    bpy.ops.mesh.select_all(action='TOGGLE')
    bpy.ops.mesh.select_mode(type = 'FACE')
        
    obj = bpy.context.edit_object
    msh = obj.data
    bm = bmesh.from_edit_mesh(msh)
    bm.faces[8].select = True
    bmesh.update_edit_mesh(msh, True)
    
    return bm.faces[8]

def get_top_face_idx():
    obj = bpy.context.edit_object
    msh = obj.data
    bm = bmesh.from_edit_mesh(msh)
    bm.normal_update()
    
    idx = -1
    z_vec = mathutils.Vector((0.0, 0.0, 1.0))
    for i in range(len(bm.faces)):
        n = bm.faces[i].normal
        if(n.dot(z_vec) > 0.5):
            idx = i
            break
        
    return idx
        
    
def extrude_trunk(dist):
    
    r_angle = random.random() * 360.0
    
    vec_x = mathutils.Vector((1., 0., 0.))
    mat_rot = mathutils.Matrix.Rotation(
        math.radians(r_angle), 
        4, 'Z')
    rot_axis = mat_rot * vec_x
    
    # tilt face a bit
    bpy.ops.transform.rotate(
        value = -0.15,
        axis = rot_axis
    )
    
    # shrink
    bpy.ops.transform.resize(
        value = (0.9, 0.9, 0.9)
    )
    # extrude
    obj = bpy.context.edit_object
    msh = obj.data
    bm = bmesh.from_edit_mesh(msh)
    bm.normal_update()
    
    top_idx = get_top_face_idx()
    trans_vec = bm.faces[top_idx].normal * dist
    
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={
            "value": trans_vec
            }
        )
        
    bm.normal_update()
    
    # tilt face a bit
    bpy.ops.transform.rotate(
        value = 0.15,
        axis = rot_axis
    )
    
def create_cone():
    bpy.ops.mesh.primitive_cone_add(
        vertices = 10,
        location = ((0, 0, 0))
    )

if __name__=='__main__':
    delete_everything()
    create_cone()
    
    # triangulate, then subdivide
    edit_mode()
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
    bpy.ops.object.modifier_add(type='DISPLACE')
    bpy.ops.texture.new()
    bpy.ops.texture.new()
    bpy.context.object.modifiers["Displace"].direction = 'Z'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
