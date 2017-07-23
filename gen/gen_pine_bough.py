'''
Emily Donahue, 2016
Blender script to generate a pine bough
'''

import bpy
import bmesh
import mathutils
import math
import random

from blendutils import *

scene = bpy.context.scene
   
def create_cone():
    bpy.ops.mesh.primitive_cone_add(
        vertices = 10,
        location = ((0, 0, 0))
    )
    
    bpy.context.object.name = 'bough'

# if __name__=='__main__':
def gen_pine_bough():
    # delete_everything()
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
    bpy.data.textures[-1].type = 'CLOUDS'
    bpy.data.textures[-1].noise_scale = random.random()
    bpy.context.object.modifiers["Displace"].texture = \
        bpy.data.textures[-1]
    bpy.context.object.modifiers["Displace"].direction = 'Z'
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Displace")
        
    # move over
    bpy.ops.transform.translate(
        value=(0, -2, 0)
    )
    bpy.ops.transform.resize(
        value=(1, 0.5, 1)
    )
    
    select_none()
        
    # create UV sphere
    bpy.ops.mesh.primitive_uv_sphere_add(
        size=1, 
        location=(0, 0, 0)
    )
    bpy.context.object.name = 'sphere'
    
    # shrinkwrap
    select_none()
    bpy.context.scene.objects.active = bpy.data.objects['bough']
    
    bpy.ops.object.modifier_add(type='SHRINKWRAP')
    bpy.context.object.modifiers["Shrinkwrap"].target = bpy.data.objects['sphere']
    bpy.context.object.modifiers["Shrinkwrap"].offset = 1
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Shrinkwrap")
    
    # delete sphere
    select_none()
    bpy.data.objects['sphere'].select=True
    bpy.ops.object.delete()
    
    # re-position bough
    select_none()
    bpy.data.objects['bough'].select=True
    bpy.ops.transform.rotate(
        value=math.radians(45), 
        axis=(1, 0, 0), 
        constraint_axis=(True, False, False)
    )
    bpy.ops.transform.translate(
        value=(0, 2.5, -0.85)
    )
    
