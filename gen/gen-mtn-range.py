'''
Emily Donahue, 2016
Blender script to procedurally generate a mountainous terrain.
'''

import bpy
import bmesh
import mathutils
import math
import random

scene = bpy.context.scene

# numeric definitinos for mountain placement options
EVERYWHERE=0
BORDER=1
CENTER=2
LINE=3

def delete_everything():
    if not scene.objects:
        return
    for ob in scene.objects:
        ob.select = True
    bpy.ops.object.mode_set(mode = 'OBJECT')
    bpy.ops.object.delete()
    
def select_all():
    for ob in scene.objects:
        ob.select = True
        
def select_none():
    for ob in scene.objects:
        ob.select = False
        
def filter_selection(where, param=None):
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

def raise_middle(dz=2.0, size=15.0):
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all()
    filter_selection(CENTER, param = 1.0)
    bpy.ops.transform.translate(
            value=(0.0, 0.0, dz),
            constraint_axis=(False, False, True), # constrain along Z
            constraint_orientation='GLOBAL',
            proportional='ENABLED',
            proportional_edit_falloff='SPHERE',
            proportional_size=size
        )
    bpy.ops.mesh.select_all(action='DESELECT')

def bump(iters, pct, dz, size, prop_falloff='SMOOTH',
        where=EVERYWHERE, where_param=None):
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

def create_ground(origin, ratio=2):
    n_subdiv = 32
    
    bpy.ops.mesh.primitive_grid_add(
        radius=15.0,
        enter_editmode=False,
        location=origin,
        x_subdivisions=(ratio * n_subdiv),
        y_subdivisions=n_subdiv
    )

    bpy.ops.transform.resize(
        value=(float(ratio), 1.0, 1.0)
    )
    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.quads_convert_to_tris(use_beauty=True)
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # create some main peaks
    raise_middle()
    
    bump_loc=CENTER
    
    # bump(iters=1, pct=1.0, dz=3.2, size=4.0, where=bump_loc,
    #     where_param=3.0)
    bump(iters=5, pct=2.5, dz=0.9, size=2.4, \
        prop_falloff='SPHERE', where=bump_loc, \
        where_param=7.5)
    bump(iters=3, pct=1.0, dz=0.5, size=3.0)
    bump(iters=5, pct=5.0, dz=0.1, size=2.5, prop_falloff='RANDOM')
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    
if __name__=='__main__':
    # delete_everything()
    create_ground((0.0,0.0,0.0), ratio=2.5)