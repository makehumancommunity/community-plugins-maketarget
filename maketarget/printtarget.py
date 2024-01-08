#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy


class MHC_OT_PrintSelectedTargetOperator(bpy.types.Operator):
    """Print all differing vertices to console"""
    bl_idname = "mh_community.print_selected_target"
    bl_label = "Print selected target"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if obj is not None:
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh":
                    if obj.data.shape_keys and obj.data.shape_keys.key_blocks and obj.active_shape_key_index != 0:
                        return True

        return False

    def execute(self, context):

        obj = context.active_object
        sks = obj.data.shape_keys
        bt = sks.key_blocks["Basis"]
        idx = obj.active_shape_key_index
        pt = sks.key_blocks[idx]

        numverts = len(bt.data)
        i = 0
        while i < numverts:
            btvco = bt.data[i].co
            ptvco = pt.data[i].co
            if btvco != ptvco:
                diffco = ptvco - btvco
                print(str(i) + " " + str(diffco))
            i = i + 1

        self.report({'INFO'}, "Target printed to console")
        return {'FINISHED'}
