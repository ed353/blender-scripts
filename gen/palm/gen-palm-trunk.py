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
import imp
imp.reload(blendutils)
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
    
  bm = bmesh_from_object(obj)

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

def half_turn(obj):

  select_none()
  set_active_object(obj)

  # rotate half-turn about z
  r_degrees = 18.0 * idx
  r_radians = math.radians(r_degrees)
  bpy.ops.transform.rotate(
    value=r_radians,
    axis=(0, 0, 1),
    proportional='DISABLED'
  )
  
  select_none()

def tilt(obj, idx, tilt_scale, tilt_offset, axis_origin):

  tilt_axis = mathutils.Vector((1, 0, 0))
  tilt_angle = (tilt_scale * idx) - tilt_offset
  tilt_radians = math.radians(tilt_angle)
  
  # set object origin to axis_origin
  prev_cursor_location = bpy.context.scene.cursor_location
  cursor_to(axis_origin)
  bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  
  bpy.ops.transform.rotate(
    value=tilt_radians,
    axis=tilt_axis,
    constraint_orientation='GLOBAL',
    proportional='DISABLED'
  )
  
  # reset cursor location and object origin
  bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
  cursor_to(prev_cursor_location)

def squeeze(obj, ratio):
  
  select_none()
  set_active_object(obj)
  edit_mode()
  select_none()
  bpy.ops.mesh.select_mode(type='FACE')

  bm = bmesh_from_object(obj)
  top_idx = get_top_face_idx(bm)
  bm.faces.ensure_lookup_table()
  bm.faces[top_idx].select = True

  bpy.ops.transform.resize(
    value=((ratio, ratio, ratio)),
    constraint_orientation='GLOBAL',
    proportional='DISABLED'
  )
  
  bmesh.update_edit_mesh(obj.data, True)
  bm.free()

  object_mode()

def elongate(obj, val):

  select_none()
  set_active_object(obj)

  bpy.ops.transform.resize(
    value=(val, val, val),
    constraint_axis=(False, False, True),
    constraint_orientation='LOCAL',
    proportional='DISABLED'
  )

  select_none()

def shrink(obj, val, shrink_origin):

  select_none()
  set_active_object(obj)

  # set object origin to axis_origin
  prev_cursor_location = bpy.context.scene.cursor_location
  cursor_to(shrink_origin)
  bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
  
  bpy.ops.transform.resize(
    value=(val, val, val),
    constraint_axis=(True, True, True),
    constraint_orientation='LOCAL',
    proportional='DISABLED'
  )
  
  # reset cursor location and object origin
  bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
  cursor_to(prev_cursor_location)

  select_none()

if __name__=='__main__':
    
    delete_everything()
    
    prev_top = mathutils.Vector((0.0, 0.0, 0.0))

    n_chunks = 10
    elongate_ratio=2.5
    shrink_ratio=0.95
    squeeze_ratio=1.1
    tilt_scale=5.
    tilt_offset=(n_chunks / 2) * tilt_scale

    for idx in range(n_chunks):
      
      # make a chunk of le palm tree
      chunk = make_chunk_at(prev_top)
      elongate(chunk, elongate_ratio)
      half_turn(chunk)
      shrink(chunk, shrink_ratio**idx, prev_top)
      squeeze(chunk, squeeze_ratio)
      tilt(chunk, idx, tilt_scale, tilt_offset, prev_top)
      prev_top = get_top_center(chunk)
      elongate(chunk, 1.1)
      
