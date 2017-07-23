'''
Emily Donahue, 2016
Blender script to procedurally generate a mountainous terrain.
'''

import bpy
import bmesh
import mathutils
import math
import random

# import blendutils as butils
from blendutils import *

scene = bpy.context.scene

def delete_everything():
    if not scene.objects or len(scene.objects) == 0:
        return
    for ob in scene.objects:
        ob.select = True
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.delete()
            
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

if __name__=='__main__':
    delete_everything()
    start_tree()
    
    dist = 2.0
    for i in range(20):
        extrude_trunk(dist)
        dist = dist * 0.95
        
    object_mode()
    select_none()
    
    '''  
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.select_all(action='TOGGLE')
    
    start_tree(scale=0.75)
    dist = 0.75 * 2.0
    for i in range(20):
        extrude_trunk(dist)
        dist = dist * 0.95
    '''
    