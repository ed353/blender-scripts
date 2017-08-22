'''
Emily Donahue, 2016

Module to contain useful Blender functions
'''

import bpy
import bmesh
import mathutils
import math
import random


def object_mode():
  bpy.ops.object.mode_set(mode = 'OBJECT')

def edit_mode():
  bpy.ops.object.mode_set(mode = 'EDIT')

def select_all():
  mode = bpy.context.mode
  if mode == 'OBJECT':
    bpy.ops.object.select_all(action='SELECT')
  elif mode == 'EDIT_MESH':
    bpy.ops.mesh.select_all(action='SELECT')

def select_none():
  mode = bpy.context.mode
  if mode == 'OBJECT':
    bpy.ops.object.select_all(action='DESELECT')
  elif mode == 'EDIT_MESH':
    bpy.ops.mesh.select_all(action='DESELECT')

def delete_everything():
  select_all()
  bpy.ops.object.delete(use_global=False)

# scene = bpy.context.scene
def cursor_to_origin(scene):
  scene.cursor_location = ((0.0, 0.0, 0.0))

def select(name):
  select_none()
  bpy.context.scene.objects.active = bpy.data.objects[name]
