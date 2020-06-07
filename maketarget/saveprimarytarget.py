#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras, os, re
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty

class MHC_OT_SavePrimaryTargetOperator(bpy.types.Operator, ExportHelper):
    """Save the required shape key to a file (i.e export a target)"""
    bl_idname = "mh_community.save_primary_target"
    bl_label = "Save primary target"

    filter_glob : StringProperty(default='*.target', options={'HIDDEN'})
    filename_ext = ".target"

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

    def invoke(self, context,event):
        primtarget = context.active_object.MhPrimaryTargetName
        #
        # set the relative path for the outputfile, this could be changed to reach MH custom
        # path directly
        #
        self.filepath = bpy.path.clean_name(primtarget, replace="-") + ".target"
        return super().invoke(context, event)

    def execute(self, context):

        scaleFactor = 1.0

        if hasattr(bpy.context.scene, "MhScaleMode"):
            scaleMode = str(bpy.context.scene.MhScaleMode)

            if scaleMode == "METER":
                scaleFactor = 10.0

            if scaleMode == "CENTIMETER":
                scaleFactor = 0.1

        obj = context.active_object
        sks = obj.data.shape_keys
        primtarget = obj.MhPrimaryTargetName
        bt = sks.key_blocks["Basis"]
        pt = sks.key_blocks[primtarget]

        with open(self.filepath,"w") as f:
            f.write("# This is a target file for MakeHuman. It was written by MakeTarget2, which is a\n")
            f.write("# part of the MakeHuman Community plugin for Blender.\n#\n")
            f.write("# basemesh hm08\n")
            numverts = len(bt.data)
            i = 0
            while i < numverts:
                btvco = bt.data[i].co
                ptvco = pt.data[i].co
                if btvco != ptvco:
                    diffco = ptvco - btvco

                    # write notation used by makehuman
                    #
                    x = str(round (diffco[0] * scaleFactor, 3))
                    y = str(round (-diffco[1] * scaleFactor, 3))
                    z = str(round (diffco[2] * scaleFactor, 3))

                    if x == "0.0" or x == "-0.0":
                        x = "0"
                    elif x.startswith("-0."):
                        x = x.replace("-0", "-")
                    elif x.startswith("0."):
                        x = x.replace("0.", ".")

                    if y == "0.0" or y == "-0.0":
                        y = "0"
                    elif y.startswith("-0."):
                        y = y.replace("-0", "-")
                    elif y.startswith("0."):
                        y = y.replace("0.", ".")

                    if z == "0.0" or z == "-0.0":
                        z = "0"
                    elif z.startswith("-0."):
                        z = z.replace("-0", "-")
                    elif z.startswith("0."):
                        z = z.replace("0.", ".")
                    if (not (x == "0" and y == "0" and z == "0")):
                        f.write(str(i) + " " + x + " " + z + " " + y + "\n")
                i = i + 1

        self.report({'INFO'}, "Target " + primtarget + " saved as " + self.filepath)
        return {'FINISHED'}
