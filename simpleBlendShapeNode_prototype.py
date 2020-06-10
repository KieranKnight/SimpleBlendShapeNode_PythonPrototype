
import maya.OpenMaya as OpenMaya  
import maya.OpenMayaMPx as OpenMayaMPx  

class SimpleBlendShapeNode(OpenMayaMPx.MPxDeformerNode): 
    kPluginNodeId = OpenMaya.MTypeId(0x00000012)  
    kPluginNodeTypeName = "simpleBlendShapeNode"
    def __init__(self):  
        OpenMayaMPx.MPxDeformerNode.__init__( self )

    def deform(self, data, itGeo, localToWorldMatrix, geomIndex):
        handle_blend_mesh = data.inputValue(self.attr_mesh_blend)
        input_blend_mesh = handle_blend_mesh.asMesh()
        if not input_blend_mesh.isNull():
            fn_mesh = OpenMaya.MFnMesh(input_blend_mesh)
            points_to_blend = OpenMaya.MPointArray()
            fn_mesh.getPoints(points_to_blend)  # getting all mesh points.
            blend_weights = data.inputValue(self.attr_weight_blend).asFloat()
            envelope = OpenMayaMPx.cvar.MPxGeometryFilter_envelope  
            envelope_val = data.inputValue(envelope).asFloat()  
            mesh_points = OpenMaya.MPoint()
            mesh_weight = None
            while itGeo.isDone() == False:
                mesh_points = itGeo.position()
                mesh_weight = self.weightValue(data, geomIndex, itGeo.index())
                mesh_points += (points_to_blend[itGeo.index()] - mesh_points) * blend_weights * envelope_val * mesh_weight
                itGeo.setPosition(mesh_points)
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

    outMesh = OpenMayaMPx.cvar.MPxGeometryFilter_outputGeom  
    SimpleBlendShapeNode.attr_mesh_blend = type_attr.create('blendMesh', 'blendMesh', OpenMaya.MFnData.kMesh)
    SimpleBlendShapeNode.addAttribute(SimpleBlendShapeNode.attr_mesh_blend)
    SimpleBlendShapeNode.attributeAffects(SimpleBlendShapeNode.attr_mesh_blend, outMesh)
    SimpleBlendShapeNode.attr_weight_blend = numeric_attr.create('blendValue', 'blendValue', OpenMaya.MFnNumericData.kFloat)
    numeric_attr.setKeyable(True)
    numeric_attr.setMin(0.0)
    numeric_attr.setMax(1.0)
    SimpleBlendShapeNode.addAttribute(SimpleBlendShapeNode.attr_weight_blend)
    SimpleBlendShapeNode.attributeAffects(SimpleBlendShapeNode.attr_weight_blend, outMesh)
    
    OpenMaya.MGlobal.executeCommand("makePaintable -attrType multiFloat -sm deformer simpleBlendShapeNode weights;")

    
def initializePlugin(obj):
    """
    Initializing the plugin.
    """  
    plugin = OpenMayaMPx.MFnPlugin(obj, 'Kieran Knight', '1.0', 'Any')  
    try:  
        plugin.registerNode('simpleBlendShapeNode', SimpleBlendShapeNode.kPluginNodeId, creator, initialize, OpenMayaMPx.MPxNode.kDeformerNode)  
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
            
