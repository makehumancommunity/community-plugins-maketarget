#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras, os, re
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from .maketarget2 import calculateScaleFactor

def _saveTarget(filepath, scale, obj, selected, bt, pt):
    """
    :param obj:     get information about selected mesj
    :param bt:       basis target (shape key)
    :param pt:       the different target
    """

    bpy.ops.object.mode_set(mode='OBJECT')
    if selected:
        selectedVerts = [v.index for v in obj.data.vertices if v.select]
    else:
        selectedVerts = [v.index for v in obj.data.vertices]

    mesh = obj.MhMeshType
    mh = "Makehuman II" if mesh != "hm08" else "MakeHuman I and II"

    with open(filepath,"w") as f:
        f.write("# Target file for " + mh + ". It was written by MakeTarget2, which is a\n")
        f.write("# part of the MakeHuman Community plugin for Blender.\n#\n")
        f.write("# basemesh " + mesh + "\n")
        numverts = len(bt.data)
        i = 0
        while i < numverts:
            btvco = bt.data[i].co
            ptvco = pt.data[i].co
            if btvco != ptvco and i in selectedVerts:
                diffco = ptvco - btvco

                # write notation used by makehuman
                #
                x = str(round (diffco[0] * scale, 3))
                y = str(round (-diffco[1] * scale, 3))
                z = str(round (diffco[2] * scale, 3))

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


class MHC_OT_SaveSelectedTargetOperator(bpy.types.Operator, ExportHelper):
    """Save the required shape key to a file (i.e export a target)"""
    bl_idname = "mh_community.save_selected_target"
    bl_label = "Save selected target"

    filter_glob : StringProperty(default='*.target', options={'HIDDEN'})
    filename_ext = ".target"

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

    def invoke(self, context,event):

        obj = context.active_object

        # create a file name valid for all systems
        #
        target = obj.active_shape_key.name
        filename = "".join( x for x in target if (x.isalnum() or x in "-")).lower()

        #
        # set the relative path for the outputfile, this could be changed to reach MH custom
        # path directly
        #
        self.filepath = bpy.path.clean_name(filename, replace="-") + ".target"
        return super().invoke(context, event)

    def execute(self, context):

        obj = context.active_object
        scaleFactor = calculateScaleFactor(bpy.context.scene, obj)
        idx = obj.active_shape_key_index

        sks = obj.data.shape_keys
        target = sks.key_blocks[idx].name
        bt = sks.key_blocks["Basis"]
        pt = sks.key_blocks[idx]

        _saveTarget(self.filepath, scaleFactor, obj, obj.MhTargetSelVertsOnly, bt, pt)

        self.report({'INFO'}, "Target " + target + " saved as " + self.filepath)
        return {'FINISHED'}

class MHC_OT_SaveAllTargetsOperator(bpy.types.Operator, ExportHelper):
    """Save all shape keys to a folder (i.e export all keys as targets)"""
    bl_idname = "mh_community.save_all_targets"
    bl_label = "Save all targets to folder"

    filter_glob : StringProperty(default='*.target', options={'HIDDEN'})
    filename_ext = ".target"

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if obj is not None:
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    if obj.data.shape_keys and len(obj.data.shape_keys.key_blocks) > 1:
                        return True
        return False


    def invoke(self, context,event):
        obj = context.active_object
        if obj.active_shape_key_index == 0:
            obj.active_shape_key_index = 1

        # replace any "." to have a filename with only one suffix
        target = obj.active_shape_key.name.replace(".", "-")
        #
        # set the relative path for the outputfile, this could be changed to reach MH custom
        # path directly
        #
        self.filepath = bpy.path.clean_name(target, replace="-") + ".target"
        return super().invoke(context, event)

    def execute(self, context):

        path = self.filepath
        folder = os.path.dirname(path)

        obj = context.active_object
        scaleFactor = calculateScaleFactor(bpy.context.scene, obj)

        sks = obj.data.shape_keys
        bt = sks.key_blocks["Basis"]
        for block in obj.data.shape_keys.key_blocks:
            if block.name != "Basis":
                print (block.name)
                target = block.name.replace(".", "-")
                target = bpy.path.clean_name(target, replace="-") + ".target"
                filename = os.path.join(folder, target)
                print (filename)

                _saveTarget(filename, scaleFactor, obj, obj.MhTargetSelVertsOnly, bt, block)

        self.report({'INFO'}, "Targets saved in " + folder)
        return {'FINISHED'}

