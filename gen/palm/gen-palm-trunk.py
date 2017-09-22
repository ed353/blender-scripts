'''
Emily Donahue, 2017
Blender script to procedurally generate palm tree trunk
'''

import bpy
import bmesh
import mathutils
import math
import random

# custom module imports
import os, sys

file_path = os.getcwd() # if started from icon, cwd = ~
scripts_path = os.path.join(file_path, 'blender-scripts')
utils_path = os.path.join(scripts_path, 'utils')

if utils_path not in sys.path:
    sys.path.append(utils_path)

from blendutils import *

scene = bpy.context.scene

# def start_trunk(scale=1.0):
def make_chunk_at(bottom_origin, scale=1.0):
    
    z_trans = mathutils.Vector((0., 0., 1.))
    location = bottom_origin + z_trans
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1,
        vertices=10,
        location=location
        # enter_editmode=True
    )
    
    chunk = bpy.context.object
    select_none()
    
    return chunk

def get_top_center(chunk_obj):
    
    select_none()
    select_obj_by_name(chunk_obj.name)
    
    bpy.ops.object.mode_set(mode='EDIT')
    top_idx = get_top_face_idx()
    
    print(top_idx)
    obj = bpy.context.edit_object
    bm = bmesh.from_edit_mesh(obj.data)
    top_center = bm.faces[top_idx].calc_center_median()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return top_center

def get_top_face_idx():
    
    obj = bpy.context.edit_object
    msh = obj.data
    bm = bmesh.from_edit_mesh(msh)
    bm.normal_update()
    
    idx = -1
    z_vec = mathutils.Vector((0.0, 0.0, 1.0))
    bm.faces.ensure_lookup_table()
    for i in range(len(bm.faces)):
        n = bm.faces[i].normal
        if(n.dot(z_vec) > 0.5):
            idx = i
            break
        
    return idx

def select_obj_by_name(obj_name):
    obj = bpy.data.objects[obj_name]
    obj.select = True
    
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

if __name__=='__main__':
    
    delete_everything()
    
    prev_top = mathutils.Vector((0.0, 0.0, 0.0))

    for i in range(1):
        chunk = make_chunk_at(prev_top)
        print(chunk.name)
        
        prev_top = get_top_center(chunk)
        top_idx = get_top_idx()
        print(top_idx)
        # select_none()
        
        print(prev_top)
   
    # object_mode()
    # select_none()
