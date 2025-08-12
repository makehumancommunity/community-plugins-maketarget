#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy
import bmesh
from .symmetry_map import *
from .maketarget2 import createHelperMask



class MHC_OT_CreateTargetOperator(bpy.types.Operator):
    """Setup an (additional) shape keys (i.e create a target)"""
    bl_idname = "mh_community.create_target"
    bl_label = "Create target"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            obj = context.active_object
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    return True
        return False

    def execute(self, context):

        obj = context.active_object
        if not obj.data.shape_keys:
            basis = obj.shape_key_add(name="Basis",from_mix=False)

        target = obj.MhNewTargetName
        newtarget = obj.shape_key_add(name=target, from_mix=False)
        newtarget.value = 1.0

        # set to last index
        #
        idx = len(obj.data.shape_keys.key_blocks)-1
        obj.active_shape_key_index = idx
        target = obj.data.shape_keys.key_blocks[idx].name
        obj.MhNewTargetName = target

        if obj.MhObjectType == "Basemesh":
            createHelperMask(context)

        self.report({'INFO'},"Target " + target + " initialized")

        return {'FINISHED'}

class MHC_OT_DeleteTargetOperator(bpy.types.Operator):
    """Delete current shape keys (i.e delete this target)"""
    bl_idname = "mh_community.delete_target"
    bl_label = "Delete target"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            obj = context.active_object
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    return True
        return False

    def execute(self, context):

        obj = context.active_object
        idx = obj.active_shape_key_index
        target = obj.data.shape_keys.key_blocks[idx].name
        obj.shape_key_remove(obj.data.shape_keys.key_blocks[idx])

        # delete basis in case of last target
        #
        if len(obj.data.shape_keys.key_blocks) == 1:
            obj.shape_key_remove(obj.data.shape_keys.key_blocks[0])
        else:
            if obj.active_shape_key_index == 0:
                obj.active_shape_key_index = 1
        self.report({'INFO'},"Target " + target + " deleted")

        return {'FINISHED'}

class MHC_OT_SymmetrizeBase(bpy.types.Operator):
    """Create a symmetric base (needed when working on an exported mesh"""
    bl_idname = "mh_community.symmetrize_base"
    bl_label = "Symmetrize base"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            obj = context.active_object
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    return True
        return False

    def execute(self, context):

        obj = context.active_object
        mesh = obj.data
        bm = bmesh.new()
        bm.from_mesh(mesh)
        v = bm.verts
        v.ensure_lookup_table()
        MirrorByTable(obj, v, "r")

        bm.to_mesh(mesh)
        bm.free()
        self.report({'INFO'},"Base symmetrized")

        return {'FINISHED'}

