#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy

class MHC_OT_MergeTargets(bpy.types.Operator):
    """ Merge all targets into one """
    bl_idname = "mh_community.merge_targets"
    bl_label = "Merge targets"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        """
        must have MhObjectType and must be Basemesh
        must have at least 2 additional shapekeys
        """
        obj = context.active_object
        if obj is not None and obj.data.shape_keys:
            if not hasattr(obj, "MhObjectType"):
                return False
            if len(obj.data.shape_keys.key_blocks) < 3:
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh":
                    return True
        return False

    def execute(self, context):
        """
        get last target name and append add '_' in front
        create a new target from mix
        delete all targets except basis and new one
        rename last target to name used for last target
        """

        obj = context.active_object
        nexttarget = "_" + obj.data.shape_keys.key_blocks[-1].name

        newtarget = obj.shape_key_add(name=nexttarget, from_mix=True)
        newtarget.value = 1.0

        for shapeKey in obj.data.shape_keys.key_blocks:
            if shapeKey.name != "Basis" and shapeKey.name != nexttarget:
                obj.shape_key_remove(shapeKey)

        idx = obj.data.shape_keys.key_blocks.find(nexttarget)
        obj.data.shape_keys.key_blocks[idx].name = nexttarget[1:]
        self.report({'INFO'},"Target " + "CombinedKeys" + " combined")
        return {'FINISHED'}


