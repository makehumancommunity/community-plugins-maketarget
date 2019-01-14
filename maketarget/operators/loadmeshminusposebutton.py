import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_LoadMeshMinusPoseButton(bpy.types.Operator):
    bl_idname = "mh.load_statue_minus_pose"
    bl_label = "Load Statue Minus Pose"
    bl_description = "Make selected mesh a shapekey of active mesh, and subtract the current pose."
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.object
        #return (context.object and not context.object.MhMeshVertsDeleted)

    def execute(self, context):
        setObjectMode(context)
        try:
            loadStatueMinusPose(context)
        except MHError:
            handleMHError(context)
        return {'FINISHED'}