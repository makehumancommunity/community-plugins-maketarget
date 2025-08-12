#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Authors: Joel Palmius, black-punkduck

import bpy
import os
from . import bl_info   # to get information about version

def calculateScaleFactor(scn, obj):

    # locally defined?, then use this factor
    #
    if scn.MhTargetScaleFactor != "0":
        return(float(scn.MhTargetScaleFactor))

    # MhScaleMode in scene?
    #
    if hasattr(scn, "MhScaleMode"):
        scaleMode = str(scn.MhScaleMode)
        if scaleMode == "METER":
            return(10.0)
        elif scaleMode == "CENTIMETER":
            return(0.1)
        else:
            return(1.0)

    # scale factor defined at object
    #
    if obj is not None:
        if hasattr(obj, "MhScaleFactor"):
            return(1.0 / obj.MhScaleFactor)

    # normal case
    #
    return(1.0)

def getTargetNames(self,context):

    targetlist = []
    if context is not None and context.active_object is not None:
        obj = context.active_object
        index = 0
        sel_elem = None
        if obj.active_shape_key is not None:
            sel_elem = obj.active_shape_key.name
            targetlist.append((str(index),sel_elem,''))
            index += 1
            
        if obj.data.shape_keys is not None:
            for target in obj.data.shape_keys.key_blocks:
                if target.name != "Basis" and target.name != sel_elem:
                    index += 1
                    targetlist.append((str(index),target.name,''))
    return targetlist

def setTargetKey(self, value):
    """
    select shape key 
    """
    context = bpy.context
    targetlist = getTargetNames(self, context)
    result = None
    tval = str(value + 1) # base excluded
    for target in targetlist:
        if target[0] == tval:
            result = target[1]
            break
    if result is not None:
        obj = context.active_object
        idx = obj.data.shape_keys.key_blocks.find(result)
        context.active_object.active_shape_key_index = idx


def getTargetValue(self):
    obj = bpy.context.active_object
    if obj is not None and obj.active_shape_key is not None:
        return (obj.active_shape_key.value)
    return 1.0

def setTargetValue(self, value):
    obj = bpy.context.active_object
    if obj is not None and obj.active_shape_key is not None:
         obj.active_shape_key.value = value

def createHelperMask(context):
    bpy.ops.object.mode_set(mode='OBJECT')
    group_name = "helper_mask"
    ob = context.active_object

    # avoid creating new ones over and over
    for mod in ob.modifiers:
        if mod.type == "MASK" and mod.name == "Hide Helper":
            return

    vgrp = ob.vertex_groups
    #
    # avoid having the name before
    #
    if group_name in vgrp.keys():
        vg = vgrp[group_name]
        vgrp.remove(vg)

    grp = vgrp.new(name=group_name)
    vn = []
    for v in ob.data.vertices:
        if v.index >= 13380:            # this will not be hardcoded later
            vn.append(v.index)
    grp.add(vn, 1.0, 'ADD')
    mod = ob.modifiers.new(name='Hide Helper', type='MASK')
    mod.vertex_group = group_name
    mod.invert_vertex_group = True
    
def calculateMirrorFileName(meshtype):
    mirrorfilename =  meshtype + ".mirror"
    return os.path.join(os.path.dirname(__file__), "data", mirrorfilename)

class MHC_PT_MakeTarget_Panel(bpy.types.Panel):
    bl_label = bl_info["name"] + " v %d.%d.%d" % bl_info["version"]
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MakeTarget2"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        createBox = layout.box()
        createBox.label(text="Initialize", icon="MESH_DATA")

        base_available = False
        for obj in scn.objects:
            if hasattr(obj, "MhObjectType"):
                if obj.MhObjectType == "Basemesh" or obj.MhObjectType == "_CustomBase_":
                    base_available = True
                    break

        obj = context.active_object

        if not base_available:
            createBox.label(text="- load a base mesh first -")
            mh2box = layout.box()
            mh2box.label(text="MakeHuman Version 2 custom base", icon="MESH_DATA")
            mh2box.label(text="Assign a custom base")
            if obj is not None:
                mh2box.prop(obj, "MhCustomBase")
                mh2box.operator("mh_community.assign_custombase", text="Assign custom base")

        elif obj is None or obj.type != "MESH":
            createBox.label(text="- select the base mesh object -")
        else:

            factor = calculateScaleFactor(scn, obj)
            createBox.label(text="Current Scale: " + str(factor))
            createBox.prop(scn, "MhTargetScaleFactor", text="Scale")
            createBox.operator("mh_community.symmetrize_base", text="Symmetrize base")

            createBox.prop(obj, "MhNewTargetName")

            if obj.data.shape_keys is None:
                createBox.operator("mh_community.create_target", text="Add new target")
                createBox.operator("mh_community.load_target", text="Add target from file")
            else:
                createBox.operator("mh_community.create_target", text="Add additional target")
                createBox.operator("mh_community.load_target", text="Additional target from file")

                selBox = layout.box()
                selBox.label(text="Modify Selected Target", icon="MESH_DATA")
                selBox.prop(scn, "MhTargets", text="Select")
                selBox.prop(obj, "MhTargetValue", text="Value", slider=True)

                selBox.label(text="Symmetrize")
                selBox.operator("mh_community.symmetrize_left", text="Copy -x to +x")
                selBox.operator("mh_community.symmetrize_right", text="Copy +x to -x")

                if obj.MhObjectType == "Basemesh":
                    helBox = layout.box()
                    helBox.label(text="Helper", icon="MESH_DATA")
                    helBox.operator("mh_community.show_helper", text="Show helper")
                    helBox.operator("mh_community.hide_helper", text="Hide helper")
                    helBox.label(text="Adapt helper mesh")
                    helBox.prop(scn, "MhHelperGeometry")
                    helBox.operator("mh_community.fix_helper", text="Adapt helper mesh to base")

                saveBox = layout.box()
                saveBox.label(text="Save and merge targets", icon="MESH_DATA")

                saveBox.prop(obj, "MhTargetSelVertsOnly", text="Only selected vertices")
                saveBox.operator("mh_community.save_selected_target", text="Save selected target")
                saveBox.operator("mh_community.delete_target", text="Delete selected target")

                saveBox.operator("mh_community.merge_targets", text="Merge targets")
                saveBox.operator("mh_community.save_all_targets", text="Save all targets")

                saveBox.label(text="Debug")
                saveBox.operator("mh_community.print_selected_target", text="Print selected target")


