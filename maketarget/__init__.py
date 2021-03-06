#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: Joel Palmius

bl_info = {
    "name": "MakeTarget2",
    "author": "Joel Palmius",
    "version": (2,1,0),
    "blender": (2,80,0),
    "location": "View3D > Properties > Make Target",
    "description": "Create MakeHuman Targets",
    'wiki_url': "http://www.makehumancommunity.org/wiki/Documentation:MHBlenderTools:_MakeTarget",
    "category": "MakeHuman"}

import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from bpy.utils import register_class, unregister_class

from .maketarget2 import MHC_PT_MakeTarget_Panel
from .createprimarytarget import MHC_OT_CreatePrimaryTargetOperator
from .printprimarytarget import MHC_OT_PrintPrimaryTargetOperator
from .saveprimarytarget import MHC_OT_SavePrimaryTargetOperator
from .loadprimarytarget import MHC_OT_LoadPrimaryTargetOperator
from .symmetrizeleft import MHC_OT_SymmetrizeLeftOperator
from .symmetrizeright import MHC_OT_SymmetrizeRightOperator

MAKETARGET2_CLASSES = [
    MHC_OT_CreatePrimaryTargetOperator,
    MHC_OT_PrintPrimaryTargetOperator,
    MHC_OT_SavePrimaryTargetOperator,
    MHC_OT_LoadPrimaryTargetOperator,
    MHC_OT_SymmetrizeLeftOperator,
    MHC_OT_SymmetrizeRightOperator,
    MHC_PT_MakeTarget_Panel
]

__all__ = [
    "MHC_OT_CreatePrimaryTargetOperator",
    "MHC_OT_PrintPrimaryTargetOperator",
    "MHC_OT_SavePrimaryTargetOperator",
    "MHC_OT_LoadPrimaryTargetOperator",
    "MHC_PT_MakeTarget_Panel",
    "MHC_OT_SymmetrizeLeftOperator",
    "MHC_OT_SymmetrizeRightOperator",
    "MAKETARGET2_CLASSES"
]

def register():
    if not hasattr(bpy.types.Object, "MhPrimaryTargetName"):
        bpy.types.Object.MhPrimaryTargetName  = StringProperty(name="Target name", description="name will be used as a default for primary target and file name", default="primary_target")

    for cls in MAKETARGET2_CLASSES:
        register_class(cls)

def unregister():

    for cls in reversed(MAKETARGET2_CLASSES):
        unregister_class(cls)

if __name__ == "__main__":
    register()
    print("MakeTarget2 loaded")

