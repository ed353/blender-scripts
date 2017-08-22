'''
Emily Donahue
July 23rd, 2017

Blender script to procedurally generate a river bed terrain
'''

# Blender imports
import bpy
import bmesh

# Math-y imports
import mathutils
import math
import random

# Custom module imports
import os, sys

file_path = os.getcwd() # if started from icon, cwd = ~
scripts_path = os.path.join(file_path, 'blender/scripts')
utils_path = os.path.join(scripts_path, 'utils')

if utils_path not in sys.path:
    sys.path.append(utils_path)

# import blendutils as butils
from blendutils import *

scene = bpy.context.scene

# numeric definitinos for mountain placement options
EVERYWHERE=0
BORDER=1
CENTER=2
LINE=3
        
'''
Filter where points are selected on the mesh surface
INPUTS:
    where: location of where to select points, from 
           numeric definitions at the top of this script
    param: (optional) numeric parameter to specify how tightly
           around the location points are selected
'''
def filter_selection(where, param=None):
    
    edit_mode()
    mesh=bmesh.from_edit_mesh(bpy.context.object.data)
    selected=[v for v in mesh.verts if v.select]
    for vtx in selected:
        if(where==EVERYWHERE):
            vtx.select=True
        else:
            loc = vtx.co
            dist = loc[1]*loc[1]
            if(where==BORDER):
                r = random.random()
                p_sel = 1.0 / (1.0 + \
                    math.exp(\
                        (( -dist + param**2) / float(2.0 * param))))
                vtx.select=(r <= p_sel)
            if(where==CENTER):
                if(dist > param**2):
                    vtx.select=False
                else:
                    vtx.select=True
            if(where==LINE):
                if(abs(loc[0] - loc[1]) < param):
                    vtx.select=True
                else:
                    vtx.select=False 
    bpy.context.scene.objects.active = \
        bpy.context.scene.objects.active

def lower_middle(dz=-2.0, size=15.0):
   
    edit_mode()
    select_all()
    
    filter_selection(CENTER, param = 1.0)
    
    bpy.ops.transform.translate(
            value=(0.0, 0.0, dz),
            constraint_axis=(False, False, True), # constrain along Z
            constraint_orientation='GLOBAL',
            proportional='ENABLED',
            proportional_edit_falloff='SPHERE',
            proportional_size=size
        )
    
    select_none()
    object_mode()

def bump(iters, pct, dz, size, prop_falloff='SMOOTH',
        where=EVERYWHERE, where_param=None):
    edit_mode()
    for i in range(iters):
        bpy.ops.mesh.select_random(percent=pct)
        filter_selection(where, where_param)
        bpy.ops.transform.translate(
            value=(0.0, 0.0, dz),
            constraint_axis=(False, False, True), # constrain along Z
            constraint_orientation='GLOBAL',
            proportional='ENABLED',
            proportional_edit_falloff=prop_falloff,
            proportional_size=size
        )

def create_ground(origin, ratio=2, n_subdivisions=32):
    
    bpy.ops.mesh.primitive_grid_add(
        radius=15.0,
        enter_editmode=False,
        location=origin,
        x_subdivisions=(ratio * n_subdivisions),
        y_subdivisions=n_subdivisions
    )

    bpy.ops.transform.resize(
        value=(float(ratio), 1.0, 1.0)
    )
    
    edit_mode()

    select_all()
    bpy.ops.mesh.quads_convert_to_tris(use_beauty=True)
    select_none()

def create_bumps(bump_loc=CENTER):
    
    # deep, sharper bumps
    bump(iters=5, pct=1.0, dz=-2.0, size=5.0,
         prop_falloff='SHARP', where=bump_loc,
         where_param=2.0)
    # medium, shallower bumps
    bump(iters=5, pct=2.5, dz=-0.5, size=2.4, 
         prop_falloff='SPHERE', where=bump_loc, 
         where_param=12.0)
    # random small bumps all over
    bump(iters=5, pct=5.0, dz=-0.1, size=2.5, 
         prop_falloff='RANDOM')
    
    
if __name__=='__main__':
    
    object_mode()
    delete_everything()
    create_ground((0.0,0.0,0.0), ratio=2.0)
    
    # create main channel
    lower_middle(dz=-2.0, size=8.0)
    # create random bumps along channel of various sizes
    create_bumps()
    
    object_mode()
    
