import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_NewTargetButton(bpy.types.Operator):
    bl_idname = "mh.new_target"
    bl_label = "New Target"
    bl_description = "Create a new target and make it active."
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        return context.object

    def execute(self, context):
        global Comments
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
            Comments = []
            newTarget(context)
        except MHError:
            handleMHError(context)
        return {'FINISHED'}