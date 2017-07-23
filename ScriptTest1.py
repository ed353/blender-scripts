import bpy
from bpy import context
from math import sin, cos, radians

cubeobject = bpy.ops.mesh.primitive_ico_sphere_add

# get cursor loc - Script Modified by SardiPax
cursor = context.scene.cursor_location

radialdist = 2.0

xsize = 0.15
ysize = 0.15
zsize = 0.15

theta = 0.0
pi_over_8 = 6.28 / 16.0

levels = -10
maxlevels = 10
divi = 2.0
inci = 0.25

while levels < maxlevels:

    while theta < 6.28:
           x = cursor.x + (radialdist-(levels+ 2*cos (theta+levels/divi))) * cos (theta-levels/divi)
           y = cursor.x + (radialdist-(levels+ 2*sin (theta-levels/divi))) * sin (theta-levels/divi)
           z = cursor.z+levels
           cubeobject(location=(x, y, z))
           
           bpy.ops.transform.resize(value=(xsize* cos (theta-levels/divi), ysize* cos (theta-levels/divi),  zsize* cos (theta-levels/divi)), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1, snap=False, snap_target='CLOSEST', snap_point=(0, 0, 0), snap_align=False, snap_normal=(0, 0, 0), texture_space=False, release_confirm=False)
           theta += pi_over_8

    theta = 0.0
    levels += inci

radialdist = 1.0



