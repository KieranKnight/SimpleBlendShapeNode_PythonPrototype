# simpleBlendShapeNode
An example of creating a simple blendshape deformer using Maya's Python API

### Usage
Inside of Maya, go to Windows -> Settings -> Plugins and Preferences -> Browse
Then you want to browse to where this file is located on your machine.

Either create two objects that are different or load in a scene with a mesh
and a modified duplicated mesh. Select the first mesh (the driven object) then
the modified mesh that will be the blendshape (the dirver object) and run the following
code:
```
blend_node = cmds.deformer(type="simpleBlendShapeNode")
sel = cmds.ls(sl=True)
driver_child = cmds.listRelatives(sel[1])[0]
cmds.connectAttr("{driver}.outMesh".format(driver=driver_child), "{driven}.blendMesh".format(driven=blend_node[0]), force=True)
```

On the driven object you will find a node called simpleBlendShapeNode, this node has a blend value
attribute. The attribute goes from 0 to 1. Change the value to see the driven mesh deform into the driver.


Feel free to use this as an example! :) 
