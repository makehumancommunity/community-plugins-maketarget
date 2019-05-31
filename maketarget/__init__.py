#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehumancommunity.org/

**Github Code Home Page:**    https://github.com/makehumancommunity/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2017

**Licensing:**         AGPL3

    This file is part of MakeHuman (www.makehumancommunity.org).

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.


Abstract
--------

"""

import bpy
import os
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy.utils import register_class, unregister_class


# TODO: update documentation for WIKI cited below
bl_info = {
    "name": "Make Target 2",
    "author": "Thomas Larsson",
    "version": (2,0,0),
    "blender": (2,80,0),
    "location": "View3D > Properties > Make Target",
    "description": "Make MakeHuman Target",
    "warning": "",
    'wiki_url': "http://www.makehumancommunity.org/wiki/Documentation:MHBlenderTools:_MakeTarget",
    "category": "MakeHuman"}

BLENDER_REGION = "UI"

if bpy.app.version < (2, 80, 0):
    BLENDER_REGION = "TOOLS"

print(("Loading maketarget v %d.%d.%d" % bl_info["version"]))

from .constantsandproperties import registerMakeTargetObjectProperties, registerMakeTargetSceneProperties
from .operators import *
from .error import *

from . import mh
from . import symmetry_map
from . import utils
from . import settings
from . import proxy
from . import import_obj

from . import mt
from . import maketarget
from . import convert
from . import pose
#from . import perfect
from . import export_mh_obj

Thomas = False


class MKT_PT_MakeTargetPanel(bpy.types.Panel):
    bl_label = "Make Target  Version %d.%d.%d" % bl_info["version"]
    bl_space_type = "VIEW_3D"
    bl_region_type = BLENDER_REGION
    bl_category = "MakeTarget2"

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        ob = context.object
        if ob:
            rig = ob.parent
        else:
            rig = None
        scn = context.scene
        view = scn.view_settings

        if Thomas:
            layout.label(text="Pruning")
            row = layout.row()
            row.prop(ob, "MhPruneEnabled")
            row.prop(ob, "MhPruneWholeDir")
            row.prop(ob, "MhPruneRecursively")
            layout.operator("mh.prune_target_file")

        if not utils.isBaseOrTarget(ob):
            layout.prop(scn, "MhBodyType", text="Type")
            layout.operator("mh.import_base_obj")
            layout.operator("mh.import_base_mhclo")
            layout.operator("mh.make_base_obj")

        elif utils.isBase(ob):
            layout.label(text="Load Target")
            layout.operator("mh.new_target")
            layout.operator("mh.load_target")
            layout.operator("mh.load_target_from_mesh")
            if rig and rig.type == 'ARMATURE':
                layout.separator()
                layout.operator("mh.create_statue_from_pose")
                layout.operator("mh.load_statue_minus_pose")

        elif utils.isTarget(ob):
            if not ob.data.shape_keys:
                layout.label(text="Warning: Internal inconsistency")
                layout.operator("mh.fix_inconsistency")
                return
            layout.separator()
            box = layout.box()
            n = 0
            for skey in ob.data.shape_keys.key_blocks:
                if n == 0:
                    n += 1
                    continue
                row = box.row()
                if n == ob.active_shape_key_index:
                    icon='LIGHT'
                else:
                    icon='X'
                row.label(text="", icon=icon)
                row.prop(skey, "value", text=skey.name)
                n += 1

            layout.label(text="Load Target")
            layout.operator("mh.new_target", text="New Secondary Target")
            layout.operator("mh.load_target", text="Load Secondary From File")
            layout.operator("mh.load_target_from_mesh", text="Load Secondary From Mesh")
            ext = os.path.splitext(ob.MhFilePath)[1]
            if ext == ".mhclo":
                layout.operator("mh.fit_target")

            layout.label(text="Discard And Apply Target")
            layout.operator("mh.discard_target")
            layout.operator("mh.discard_all_targets")
            layout.operator("mh.apply_targets")

            layout.label(text="Symmetry")
            row = layout.row()
            row.operator("mh.symmetrize_target", text="Left->Right").action = "Left"
            row.operator("mh.symmetrize_target", text="Right->Left").action = "Right"
            if Thomas:
                row.operator("mh.symmetrize_target", text="Mirror").action = "Mirror"

            layout.label(text="Save Target")
            layout.prop(ob, "SelectedOnly")
            layout.prop(ob, "MhZeroOtherTargets")
            if ob["FilePath"]:
                layout.operator("mh.save_target")
            layout.operator("mh.saveas_target")

            if not ob.MhDeleteHelpers:
                layout.label(text="Skirt Editing")
                layout.operator("mh.snap_waist")
                layout.operator("mh.straighten_skirt")
                if ob.MhIrrelevantDeleted:
                    layout.separator()
                    layout.label(text="Only %s Affected" % ob.MhAffectOnly)
                else:
                    layout.label(text="Affect Only:")
                    layout.prop(ob, "MhAffectOnly", expand=True)
                    #layout.operator("mh.delete_irrelevant")


        #layout.separator()
        #layout.operator("mh.perfect_eyes")

        if rig and rig.type == 'ARMATURE':
            layout.separator()
            layout.label(text="Export/Import MHP")
            layout.operator("mh.saveas_mhp")
            layout.operator("mh.load_mhp")

            layout.separator()
            layout.label(text="Export/Import BVH")
            layout.prop(scn, "MhExportRotateMode")
            layout.operator("mh.saveas_bvh")
            layout.operator("mh.load_bvh")

            layout.separator()
            layout.label(text="Convert between rig weights")
            layout.prop(scn, "MhSourceRig")
            layout.prop(scn, "MhTargetRig")
            layout.prop(scn, "MhPoseTargetDir")
            layout.operator("mh.convert_rig")

#----------------------------------------------------------
#   class MakeTargetBatchPanel(bpy.types.Panel):
#----------------------------------------------------------

class MKT_PT_MakeTargetBatchPanel(bpy.types.Panel):
    bl_label = "Batch make targets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(self, context):
        return context.scene.MhUnlock and maketarget.isInited(context.scene)

    def draw(self, context):
        if utils.isBase(context.object):
            layout = self.layout
            scn = context.scene
            #for fname in maketarget.TargetSubPaths:
            #    layout.prop(scn, "Mh%s" % fname)
            layout.prop(scn, "MhTargetPath")
            layout.operator("mh.batch_fix")
            layout.operator("mh.batch_render", text="Batch Render").opengl = False
            layout.operator("mh.batch_render", text="Batch OpenGL Render").opengl = True

#-------------------------------#----------------------------------------------------------
#   class McpPanel(bpy.types.Panel):
#----------------------------------------------------------

class MKT_PT_McpPanel(bpy.types.Panel):
    bl_label = "Export/Import MCP"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    @classmethod
    def poll(self, context):
        return (context.object and context.object.type == 'ARMATURE')

    def draw(self, context):
        layout = self.layout
        layout.operator("mh.saveas_mhp")
        layout.operator("mh.load_mhp")
        layout.separator()
        layout.operator("mh.write_matrices")

#----------------------------------------------------------
#   class ExportObj(bpy.types.Operator, ExportHelper):
#----------------------------------------------------------

class MKT_OT_ExportObj(bpy.types.Operator, ExportHelper):
    '''Export to OBJ file format (.obj)'''
    bl_idname = "mh.export_obj"
    bl_description = 'Export to OBJ file format (.obj)'
    bl_label = "Export MH OBJ"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"

    filename_ext = ".obj"
    filter_glob : StringProperty(default="*.obj", options={'HIDDEN'})
    filepath : StringProperty(name="File Path", description="File path for the exported OBJ file", maxlen= 1024, default= "")

    groupsAsMaterials : BoolProperty(name="Groups as materials", default=False)

    def execute(self, context):
        utils.setObjectMode(context)
        export_mh_obj.exportObjFile(self.properties.filepath, self.groupsAsMaterials, context)
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#----------------------------------------------------------
#   Register
#----------------------------------------------------------

def menu_func(self, context):
    self.layout.operator(MKT_OT_ExportObj.bl_idname, text="MakeHuman OBJ (.obj)...")

classes = [
    MKT_PT_MakeTargetPanel,
    MKT_PT_MakeTargetBatchPanel,
    MKT_PT_McpPanel,
    MKT_OT_ExportObj,
    ErrorOperator
]

classes.extend(MAKETARGET_OPERATOR_CLASSES)

def register():

    for cls in classes:
        register_class(cls)

    registerMakeTargetObjectProperties()
    registerMakeTargetSceneProperties()

    #maketarget.init()
    #try:
    #    maketarget.initBatch(bpy.context.scene)
    #except:
    #    pass
    #bpy.utils.register_module(__name__)
    #bpy.types.INFO_MT_file_export.append(menu_func)


def unregister():

    for cls in reversed(classes):
        unregister_class(cls)


if __name__ == "__main__":
    register()
    print("MakeTarget loaded")

