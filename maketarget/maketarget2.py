#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: Joel Palmius

import bpy
from . import bl_info   # to get information about version

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
                if obj.MhObjectType == "Basemesh":
                    base_available = True
                    break

        obj = context.active_object

        if not base_available:
            createBox.label(text="- load a base mesh first -")
        elif obj is None or obj.type != "MESH":
            createBox.label(text="- select the base mesh object -")
        else:
            createBox.prop(obj, "MhPrimaryTargetName")
            createBox.operator("mh_community.create_primary_target", text="Create target")
            createBox.operator("mh_community.load_primary_target", text="Load target")

            saveBox = layout.box()
            saveBox.label(text="Save Target", icon="MESH_DATA")
            saveBox.operator("mh_community.save_primary_target", text="Save target")

            symmetrizeBox = layout.box()
            symmetrizeBox.label(text="Symmetrize", icon="MESH_DATA")
            symmetrizeBox.operator("mh_community.symmetrize_left", text="Copy -x to +x")
            symmetrizeBox.operator("mh_community.symmetrize_right", text="Copy +x to -x")

            debugBox = layout.box()
            debugBox.label(text="Debug Target", icon="MESH_DATA")
            debugBox.operator("mh_community.print_primary_target", text="Print target")

