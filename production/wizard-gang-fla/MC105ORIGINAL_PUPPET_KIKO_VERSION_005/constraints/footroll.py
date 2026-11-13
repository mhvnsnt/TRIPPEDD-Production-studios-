#BPYCONSTRAINT
'''
	Makes the heel bone of a foot "roll" when rotated.
	
	Notes:
	- The Z axis of the heel bone must be pointing down.
	- Make sure that the "length" setting of this constraint
	  matches the rest length of the heel bone.
	- Use in local space.
'''

import Blender
from Blender import Draw
import math




def doConstraint(obmatrix, targetmatrix, idprop):
	# Get the "length" setting.
	if not idprop.has_key('length'): idprop['length'] = 1.0
	
	# Get the rotation and scale of the bone.
	rotation = obmatrix.toEuler()
	scale = obmatrix.scalePart()
	
	# Foot roll!
	if rotation.x > 0:
		obmatrix[3].z -= (math.sin((rotation.x/180)*math.pi)) * idprop['length'] * scale.y
		obmatrix[3].y += (1 - math.cos((rotation.x/180)*math.pi)) * idprop['length'] * scale.y
	
	return obmatrix;




def getSettings(idprop):
	if not idprop.has_key('length'): idprop['length'] = 1.0
	
	# create temporary vars for interface 
	blength = Draw.Create(idprop['length'])


	# define and draw pupblock
	block = []
	block.append(("Bone length", blength, 0.0000001, 1000.0, "Set this to the rest length of the bone."))

	retval = Draw.PupBlock("Foot Roll Constraint", block)
	
	# update id-property values after user changes settings
	if (retval):
		idprop['length']= blength.val
 
