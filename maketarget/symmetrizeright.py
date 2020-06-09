#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from .symmetry_map import *

class MHC_OT_SymmetrizeRightOperator(bpy.types.Operator):
    """Symmetrize target by copying inverted vertex positions from left (+x) to right (-x)"""
    bl_idname = "mh_community.symmetrize_right"
    bl_label = "Copy +x to -x"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if obj is not None:
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh":
                    primtarget = obj.MhPrimaryTargetName
                    if obj.data.shape_keys and obj.data.shape_keys.key_blocks and primtarget in obj.data.shape_keys.key_blocks:
                        return True
        return False

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = context.active_object
        sks = obj.data.shape_keys
        primtarget = obj.MhPrimaryTargetName
        pt = sks.key_blocks[primtarget]
        (b, name) =  MirrorByTable(obj, pt, "l")
        if b == False:
            self.report({'ERROR'}, "Mirror-config missing: " + name)
            return {'CANCELLED'}

        self.report({'INFO'}, "Target symmetrized")
        return {'FINISHED'}
