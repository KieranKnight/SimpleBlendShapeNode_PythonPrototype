"""
MIT License

Copyright (c) 2020 KieranKnight

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

------------------------------------------------------------------------------
Creating a Simple Blendshape deformer node.

Description:
This module is an example of how to create a simple blendshape deformation node
with deformation influence from paint weights using Maya's Python API.
"""

import maya.OpenMaya as OpenMaya  
import maya.OpenMayaMPx as OpenMayaMPx  

class SimpleBlendShapeNode(OpenMayaMPx.MPxDeformerNode):
    # Plugin node information 
    kPluginNodeId = OpenMaya.MTypeId(0x00000012)  
    kPluginNodeTypeName = "simpleBlendShapeNode"
    def __init__(self):  
        OpenMayaMPx.MPxDeformerNode.__init__( self )

    def deform(self, data, itGeo, localToWorldMatrix, geomIndex):
        # grabbing the handles to the attr value attribute
        handle_blend_mesh = data.inputValue(self.attr_mesh_blend)
        input_blend_mesh = handle_blend_mesh.asMesh()

        # checking that there is an input mesh
        if not input_blend_mesh.isNull():
            # taking the input mesh and creating a MFnMesh object
            fn_mesh = OpenMaya.MFnMesh(input_blend_mesh)
            points_to_blend = OpenMaya.MPointArray()
            fn_mesh.getPoints(points_to_blend)  # getting all mesh points.

            # getting the weight from the driven mesh that will be influenced
            # by the driver mesh
            blend_weights = data.inputValue(self.attr_weight_blend).asFloat()
            # getting the envelope...
            envelope = OpenMayaMPx.cvar.MPxGeometryFilter_envelope  
            envelope_val = data.inputValue(envelope).asFloat()  

            mesh_points = OpenMaya.MPoint()
            mesh_weight = None
            # checking that all verticies
            while itGeo.isDone() == False:
                mesh_points = itGeo.position()  # getting the current position
                # getting teh current vertext position weight value
                mesh_weight = self.weightValue(data, geomIndex, itGeo.index())
                # calculating the driver to the driven
                mesh_points += (points_to_blend[itGeo.index()] - mesh_points) * blend_weights * envelope_val * mesh_weight
                itGeo.setPosition(mesh_points)  # setting the position
                itGeo.next()  # going to the next index
            
def creator():  
    """
    The Creator function to initialize the class SimpleBlendShapeNode

    Returns:
        OpenMayaMPx Pointer: A pointer to the SimpleBlendShapeNode class
    """
    return OpenMayaMPx.asMPxPtr(SimpleBlendShapeNode())  

    
def initialize():   
    """
    Initializing the node inside of Maya.
    This creates all attributes and values avaliable to the custom node.
    """
    numeric_attr = OpenMaya.MFnNumericAttribute()  
    type_attr = OpenMaya.MFnTypedAttribute()

    outMesh = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom  # The driven output geometry
    
    # Creatting the blendMesh and blendValue attributes for the node
    SimpleBlendShapeNode.attr_mesh_blend = type_attr.create('blendMesh', 'blendMesh', OpenMaya.MFnData.kMesh)
    SimpleBlendShapeNode.addAttribute(SimpleBlendShapeNode.attr_mesh_blend)
    SimpleBlendShapeNode.attributeAffects(SimpleBlendShapeNode.attr_mesh_blend, outMesh)
    SimpleBlendShapeNode.attr_weight_blend = numeric_attr.create('blendValue', 'blendValue', OpenMaya.MFnNumericData.kFloat)
    numeric_attr.setKeyable(True)
    numeric_attr.setMin(0.0)
    numeric_attr.setMax(1.0)
    # Adding the attributes back to the class object.
    SimpleBlendShapeNode.addAttribute(SimpleBlendShapeNode.attr_weight_blend)
    SimpleBlendShapeNode.attributeAffects(SimpleBlendShapeNode.attr_weight_blend, outMesh)
    
    # Enabling Maya's paint weights to have influence on the blendshape node.
    OpenMaya.MGlobal.executeCommand("makePaintable -attrType multiFloat -sm deformer simpleBlendShapeNode weights;")

    
def initializePlugin(obj):
    """
    Initializing the plugin.
    """  
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Kieran Knight', '1.0', 'Any')  
    try:  
        plugin.registerNode(
            'simpleBlendShapeNode', 
            SimpleBlendShapeNode.kPluginNodeId, 
            creator, 
            initialize, 
            OpenMayaMPx.MPxNode.kDeformerNode
        )  
    except:  
        raise RuntimeError, 'Failed to register node'  

            
def uninitializePlugin(obj):
    """
    Uninitializing the plugin.
    """
    plugin = OpenMayaMPx.MFnPlugin(obj)  
    try:  
        plugin.deregisterNode(SimpleBlendShapeNode.kPluginNodeId)  
    except:  
        raise RuntimeError, 'Failed to deregister node'  
            
