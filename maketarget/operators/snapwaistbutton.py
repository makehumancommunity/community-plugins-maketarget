import bpy
from ..utils import *
from ..error import *
from bpy.props import *

class VIEW3D_OT_SnapWaistButton(bpy.types.Operator):
    bl_idname = "mh.snap_waist"
    bl_label = "Snap Skirt Waist"
    bl_description = "Snap the top row of skirt verts to the corresponding tight verts"
    bl_options = {'UNDO'}

    @classmethod
    def poll(self, context):
        ob = context.object
        return (ob.MhAffectOnly == 'Skirt' or not ob.MhIrrelevantDeleted)

    def execute(self, context):
        try:
            setObjectMode(context)
            snapWaist(context)
        except MHError:
            handleMHError(context)
        return{'FINISHED'}