import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_CreateStatueFromPoseButton(bpy.types.Operator):
    bl_idname = "mh.create_statue_from_pose"
    bl_label = "Create Statue From Pose"
    bl_description = "Apply the current pose to the mesh"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.object
        #return (context.object and not context.object.MhMeshVertsDeleted)

    def execute(self, context):
        setObjectMode(context)
        try:
            createStatueFromPose(context)
        except MHError:
            handleMHError(context)
        return {'FINISHED'}