#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: Joel Palmius

bl_info = {
    "name": "MakeTarget2",
    "author": "Joel Palmius, black-punkduck",
    "version": (3,1,0),
    "blender": (2,80,0),
    "location": "View3D > Properties > Make Target",
    "description": "Create MakeHuman Targets",
    'wiki_url': "http://www.makehumancommunity.org/wiki/Documentation:TargetsV2",
    "category": "MakeHuman"}

import bpy
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from bpy.utils import register_class, unregister_class

from .maketarget2 import MHC_PT_MakeTarget_Panel, getTargetNames, getTargetValue, setTargetValue, setTargetKey
from .createtarget import MHC_OT_CreateTargetOperator, MHC_OT_DeleteTargetOperator,  MHC_OT_SymmetrizeBase
from .mergetargets import MHC_OT_MergeTargets
from .printtarget import MHC_OT_PrintSelectedTargetOperator
from .savetarget import MHC_OT_SaveSelectedTargetOperator, MHC_OT_SaveAllTargetsOperator
from .loadtarget import MHC_OT_LoadTargetOperator
from .fixhelper import MHC_OT_FixHelper, MHC_OT_ShowHelper, MHC_OT_HideHelper
from .symmetrizeleft import MHC_OT_SymmetrizeLeftOperator
from .symmetrizeright import MHC_OT_SymmetrizeRightOperator

MAKETARGET2_CLASSES = [
    MHC_OT_CreateTargetOperator,
    MHC_OT_DeleteTargetOperator,
    MHC_OT_SymmetrizeBase,
    MHC_OT_MergeTargets,
    MHC_OT_PrintSelectedTargetOperator,
    MHC_OT_SaveSelectedTargetOperator,
    MHC_OT_SaveAllTargetsOperator,
    MHC_OT_LoadTargetOperator,
    MHC_OT_FixHelper,
    MHC_OT_ShowHelper,
    MHC_OT_HideHelper,
    MHC_OT_SymmetrizeLeftOperator,
    MHC_OT_SymmetrizeRightOperator,
    MHC_PT_MakeTarget_Panel
]

__all__ = [
    "MHC_OT_CreateTargetOperator",
    "MHC_OT_DeleteTargetOperator",
    "MHC_OT_SymmetrizeBase",
    "MHC_OT_MergeTargets",
    "MHC_OT_PrintSelectedTargetOperator",
    "MHC_OT_SaveSelectedTargetOperator",
    "MHC_OT_SaveAllTargetsOperator",
    "MHC_OT_LoadTargetOperator",
    "MHC_PT_MakeTarget_Panel",
    "MHC_OT_FixHelper",
    "MHC_OT_ShowHelper",
    "MHC_OT_HideHelper",
    "MHC_OT_SymmetrizeLeftOperator",
    "MHC_OT_SymmetrizeRightOperator",
    "MAKETARGET2_CLASSES"
]

def register():
    if not hasattr(bpy.types.Object, "MhNewTargetName"):
        bpy.types.Object.MhNewTargetName  = StringProperty(name="Name", description="name will be used as a default for the first target and file name", default="CustomTarget.001")

    bpy.types.Scene.MhTargetScaleFactor = EnumProperty(name='Scale', default="0",
            items=[("0", "Don't change", ""), ("10", "10.0 (meters)", ""),("1", "1.0 (decimeters)", ""),("0.1", "0.1 (centimeters)", "")],
            description= "Depending how the character is loaded, a different scale must be used, MPFB works with 10.0, MakeClothes with 1.0")

    bpy.types.Scene.MhTargets = EnumProperty(name='Target', items=getTargetNames, set=setTargetKey, description= "Targets to select")

    bpy.types.Scene.MhHelperGeometry = EnumProperty(name="Type", default="basehelper",
            items=[("basehelper", "Base (Standard Pose)", ""), ("femalehelper", "Female (Standard Pose)", ""),("malehelper", "Male (Standard Pose)", "")],
            description= "Depending how the character is loaded, choose adapting geometry for helper")

    bpy.types.Object.MhTargetValue = FloatProperty(name="Target value", description="current value of the target",
            default=1.0, get=getTargetValue, set=setTargetValue, min=0.0, max=1.0)

    bpy.types.Object.MhTargetSelVertsOnly = BoolProperty(name='SelVertsOnly', description="use selected verts only", default=False)


    for cls in MAKETARGET2_CLASSES:
        register_class(cls)

def unregister():

    for cls in reversed(MAKETARGET2_CLASSES):
        unregister_class(cls)

if __name__ == "__main__":
    register()
    print("MakeTarget2 loaded")

