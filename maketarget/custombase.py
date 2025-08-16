#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy
import os

from .maketarget2 import getMirrorFileName

class MHC_OT_AssignCustomObject(bpy.types.Operator):
    """Assigns a custom object as Basemesh"""
    bl_idname = "mh_community.assign_custombase"
    bl_label = "Assign custom base"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            obj = context.active_object
            if not hasattr(obj, "MhCustomBase") or obj.MhCustomBase == "":
                return False
            return True
        return False

    def execute(self, context):
        obj = context.active_object
        print ("Assign", obj.MhCustomBase)
        obj.MhMeshType = obj.MhCustomBase
        obj.MhObjectType = "_CustomBase_"
        obj.MhMirrorFile = getMirrorFileName(obj.MhCustomBase)
        return {'FINISHED'}

