import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_StraightenSkirtButton(bpy.types.Operator):
    bl_idname = "mh.straighten_skirt"
    bl_label = "Straighten Skirt"
    bl_description = "Make (the right side of) the skirt perfectly straight."
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        ob = context.object
        return (ob.MhAffectOnly == 'Skirt' or not ob.MhIrrelevantDeleted)

    def execute(self, context):
        try:
            setObjectMode(context)
            straightenSkirt(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}