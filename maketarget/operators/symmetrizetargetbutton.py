import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_SymmetrizeTargetButton(bpy.types.Operator):
    bl_idname = "mh.symmetrize_target"
    bl_label = "Symmetrize"
    bl_description = "Symmetrize or mirror active target"
    bl_options = {'UNDO'}
    action = StringProperty()

    def execute(self, context):
        try:
            setObjectMode(context)
            symmetrizeTarget(context, (self.action=="Right"), (self.action=="Mirror"))
        except MHError:
            handleMHError(context)
        return{'FINISHED'}