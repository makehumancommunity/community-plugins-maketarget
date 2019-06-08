#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from .symmetry_map import *

class MHC_OT_SymmetrizeLeftOperator(bpy.types.Operator):
    """Symmetrize target by copying inverted vertex positions from right (-x) to left (+x)"""
    bl_idname = "mh_community.symmetrize_left"
    bl_label = "Copy -x to +x"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType == "Basemesh":
                    if context.active_object.data.shape_keys and context.active_object.data.shape_keys.key_blocks and "PrimaryTarget" in context.active_object.data.shape_keys.key_blocks:
                        return True
        return False

    def execute(self, context):

        obj = context.active_object
        sks = obj.data.shape_keys
        pt = sks.key_blocks["PrimaryTarget"]

        for s in Left2Right.items():
            leftVertNo = s[0]
            rightVertNo = s[1]

            leftco = pt.data[leftVertNo].co
            rightco = pt.data[rightVertNo].co

            leftco[0] = -rightco[0]
            leftco[1] = rightco[1]
            leftco[2] = rightco[2]

        self.report({'INFO'}, "Target symmetrized")
        return {'FINISHED'}
