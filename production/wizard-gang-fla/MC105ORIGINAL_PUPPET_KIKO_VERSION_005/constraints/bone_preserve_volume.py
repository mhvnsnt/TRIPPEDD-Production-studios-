#BPYCONSTRAINT
'''
	Forces a bone to preserve volume by automatically
	scaling it along the x and z axis'.
	
	A minimum and maximum bone width can be
	defined in constraint settings.
'''

import Blender
from Blender import Draw
from Blender import Mathutils
import math



def doConstraint(obmatrix, targetmatrix, idprop):
	# Get the user setting.
	if not idprop.has_key('minscale'): idprop['minscale'] = 0.01
	if not idprop.has_key('maxscale'): idprop['maxscale'] = 100.0
	
	# Separate out the tranformation components for easy access.
	obloc = obmatrix.translationPart()	# Translation
	obrot = obmatrix.toEuler()			# Rotation
	obsca = obmatrix.scalePart()		# Scale


	# Preserve volume!
	if obsca.y != 0:
		scale = min( max( 1 / math.fabs( obsca.y ), idprop['minscale'] ), idprop['maxscale'] )
		obsca.x = obsca.z = scale

	
	# Convert back into a matrix for loc, scale, rotation,
	mtxloc = Mathutils.TranslationMatrix( obloc )
	mtxrot = obrot.toMatrix().resize4x4()
	mtxsca = Mathutils.Matrix([obsca[0],0,0,0], [0,obsca[1],0,0], [0,0,obsca[2],0], [0,0,0,1])
	
	# Recombine the separate elements into a transform matrix.
	outputmatrix = mtxsca * mtxrot * mtxloc

	# Return the new matrix.
	return outputmatrix





def getSettings(idprop):
	if not idprop.has_key('minscale'): idprop['minscale'] = 0.01
	if not idprop.has_key('maxscale'): idprop['maxscale'] = 100.0
	
	# create temporary vars for interface 
	minscl = Draw.Create(idprop['minscale'])
	maxscl = Draw.Create(idprop['maxscale'])


	# define and draw pupblock
	block = []
	block.append(("Minimum Scale", minscl, 0.001, 10000.0, "The minimum width scale."))
	block.append(("Maximum Scale", maxscl, 0.001, 10000.0, "The maximum width scale."))

	retval = Draw.PupBlock("Volume Preserve Constraint", block)
	
	# update id-property values after user changes settings
	if (retval):
		idprop['minscale']= minscl.val
		idprop['maxscale']= maxscl.val
