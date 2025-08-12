#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras
from .symmetry_map import *

class MHC_OT_SymmetrizeLeftOperator(bpy.types.Operator):
    """Symmetrize target by copying inverted vertex positions from right (-x) to left (+x)"""
    bl_idname = "mh_community.symmetrize_left"
    bl_label = "Copy -x to +x"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if obj is not None:
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    if obj.data.shape_keys and obj.data.shape_keys.key_blocks and obj.active_shape_key_index != 0:
                        return True
        return False

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = context.active_object
        sks = obj.data.shape_keys
        idx = obj.active_shape_key_index
        pt = sks.key_blocks[idx]
        (b, name) =  MirrorByTable(obj, pt.data, "r")
        if b == False:
            self.report({'ERROR'}, "Mirror-config missing: " + name)
            return {'CANCELLED'}

        self.report({'INFO'}, "Target symmetrized")
        return {'FINISHED'}
