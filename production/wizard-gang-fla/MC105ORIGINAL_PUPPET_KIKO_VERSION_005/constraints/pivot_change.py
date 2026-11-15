#BPYCONSTRAINT

"""
	Changes the pivot point of a bone.
	Should be used in world space.
"""

import Blender
from Blender import Draw
from Blender import Mathutils
import math








def doConstraint(obmatrix, targetmatrix, idprop):
	# Separate out the tranformation components for easy access.
	obrot = obmatrix.toEuler()          # Rotation
	obscl = obmatrix.scalePart()        # Scale
	
	
	
	# Define the length parameter.
	if idprop.has_key('length')==0: idprop['length'] = 1.0;
	
	
	
	# Calculate the translation offset.
	
	offsets = [0,-idprop['length'],0]
	offset = [0,0,0]
	
	offset[2] = (offsets[2] * math.cos((obrot.x/180)*math.pi)) - (offsets[1] * (math.sin((obrot.x/180)*math.pi)))
	offset[1] = (offsets[2] * math.sin((obrot.x/180)*math.pi)) + (offsets[1] * (math.cos((obrot.x/180)*math.pi)))
	
	offsets[0] = offset[0]
	offsets[1] = offset[1]
	offsets[2] = offset[2]
	
	offset[0] = (offsets[0] * math.cos((obrot.y/180)*math.pi)) - (offsets[2] * (math.sin((obrot.y/180)*math.pi)))
	offset[2] = (offsets[0] * math.sin((obrot.y/180)*math.pi)) + (offsets[2] * (math.cos((obrot.y/180)*math.pi)))
	
	offsets[0] = offset[0]
	offsets[1] = offset[1]
	offsets[2] = offset[2]
	
	offset[0] = (offsets[0] * math.cos((obrot.z/180)*math.pi)) - (offsets[1] * (math.sin((obrot.z/180)*math.pi)))
	offset[1] = (offsets[0] * math.sin((obrot.z/180)*math.pi)) + (offsets[1] * (math.cos((obrot.z/180)*math.pi)))
	
	
	
	# Apply the translation offset.
	obmatrix[3][0] += offset[0] * obscl.y
	obmatrix[3][1] += offset[1] * obscl.y
	obmatrix[3][2] -= offset[2] * obscl.y
	


	# Return the modified matrix.
	return obmatrix;








def getSettings(idprop):
    # Define the length parameter.
	if idprop.has_key('length')==0: idprop['length'] = 1.0;
	
	
	
	# create temporary vars for interface 
	tlength = Draw.Create(float(idprop['length']));
	


	# define and draw pupblock
	block = []
	block.append("Settings: ");
	block.append(("Bone Length", tlength, 0.0, 100.0, "Length of the bone."));
   
	retval = Draw.PupBlock("Constraint Template", block);
	


	# update id-property values after user changes settings
	if (retval):
		idprop['length']= tlength.val;
	
	
		
	# 'return' here is optional
	return True;