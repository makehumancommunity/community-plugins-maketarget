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

        obj = context.active_object
        sks = obj.data.shape_keys
        primtarget = obj.MhPrimaryTargetName
        pt = sks.key_blocks[primtarget]

        for s in Left2Right.items():
            leftVertNo = s[1]
            rightVertNo = s[0]

            leftco = pt.data[leftVertNo].co
            rightco = pt.data[rightVertNo].co

            leftco[0] = -rightco[0]
            leftco[1] = rightco[1]
            leftco[2] = rightco[2]

        self.report({'INFO'}, "Target symmetrized")
        return {'FINISHED'}
