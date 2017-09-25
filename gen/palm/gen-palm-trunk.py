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
from blendutils import *

'''
Make a "chunk" of the trunk with its base at a specified location.
'''
def make_chunk_at(bottom_origin, scale=1.0):
    
    z_trans = mathutils.Vector((0., 0., 1.))
    location = bottom_origin + z_trans
    
    bpy.ops.mesh.primitive_cylinder_add(
        radius=1,
        vertices=10,
        location=location
    )

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    
    chunk = bpy.context.object
    select_none()
    
    return chunk

def get_top_center(obj):
    
  bm = bmesh.new()
  bm.from_mesh(obj.data)

  top_idx = get_top_face_idx(bm)
  top_ctr = bm.faces[top_idx].calc_center_median()
  top_ctr = obj.matrix_world * top_ctr

  return top_ctr

def get_top_face_idx(bm):
    
  bm.faces.ensure_lookup_table()
  bm.normal_update()
  
  idx = -1
  z_vec = mathutils.Vector((0.0, 0.0, 1.0))
  
  for i in range(len(bm.faces)):
    n = bm.faces[i].normal
    if(n.dot(z_vec) > 0.5):
      idx = i
      break
      
  return idx

if __name__=='__main__':
    
    delete_everything()
    
    prev_top = mathutils.Vector((0.0, 0.0, 0.0))

    for i in range(5):
      
      # make a chunk of le palm tree
      chunk = make_chunk_at(prev_top)
      # TODO: squeeze and tilt the trunk a lil
      prev_top = get_top_center(chunk)
      
   
    # object_mode()
    # select_none()
