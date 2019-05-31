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
from bpy.props import *
from .utils import getMHBlenderDirectory, getMHDirectory
from .error import *

_Paths = ["MhProgramPath", "MhUserPath", "MhTargetPath", "MhClothesDir", "MhUvsDir"]


def settingsFile(name, tool="make_target"):
    outdir = os.path.join(getMHBlenderDirectory(), "settings")
    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    return os.path.join(outdir, "%s.%s" % (tool, name))


def readDefaultSettings(context, tool):
    fname = settingsFile("settings", tool)
    try:
        fp = open(fname, "rU")
    except:
        print(("Did not find %s. Using default settings" % fname))
        return

    scn = context.scene
    for line in fp:
        words = line.split()
        prop = words[0]
        value = simpleEval(words[1])
        try:
            value = value.replace("%20", " ")
        except AttributeError:
            pass
        if hasattr(scn, prop):
            scn[prop] = value
    fp.close()
    return


def simpleEval(expr):
    if expr == "True":
        return True
    elif expr == "False":
        return False
    elif expr == "None":
        return None
    elif expr == "{}":
        return {}
    elif expr == "[]":
        return []

    try:
        return int(expr)
    except ValueError:
        pass

    try:
        return float(expr)
    except ValueError:
        pass

    if expr[0] in ['"',"'"] and expr[-1] == expr[0]:
        return expr[1:-1]

    raise MHError("Unable to evaluate:\n  %s" % expr)


def saveDefaultSettings(context, tool, prefix):
    fname = settingsFile("settings", tool)
    fp = open(fname, "w", encoding="utf-8", newline="\n")
    scn = context.scene
    for key in _Paths:
        saveAttr(scn, key, fp)
    for key in dir(scn):
        if key[0:2] == prefix and key[2:6] != "Show":
            saveAttr(scn, key, fp)
    fp.close()
    return


def saveAttr(scn, key, fp):
    value = getattr(scn, key)
    try:
        value = '"' + value.replace(" ", "%20").replace("\\", "/") + '"'
    except AttributeError:
        pass
    fp.write("%s %s\n" % (key, value))


def restoreFactorySettings(context, prefix):
    scn = context.scene
    for key in _Paths:
        _,props = getattr(bpy.types.Scene, key)
        setattr(scn, key, props["default"])
    for key in dir(scn):
        if key[0:2] == prefix and key[2:6] != "Show":
            _,props = getattr(bpy.types.Scene, key)
            setattr(scn, key, props["default"])


#----------------------------------------------------------
#   Settings buttons
#----------------------------------------------------------

class OBJECT_OT_FactorySettingsButton(bpy.types.Operator):
    bl_idname = "mh.factory_settings"
    bl_label = "Restore Factory Settings"

    prefix : StringProperty()

    def execute(self, context):
        restoreFactorySettings(context, self.prefix)
        return{'FINISHED'}


class OBJECT_OT_SaveSettingsButton(bpy.types.Operator):
    bl_idname = "mh.save_settings"
    bl_label = "Save Settings"

    tool : StringProperty()
    prefix : StringProperty()

    def execute(self, context):
        saveDefaultSettings(context, self.tool, self.prefix)
        return{'FINISHED'}


class OBJECT_OT_ReadSettingsButton(bpy.types.Operator):
    bl_idname = "mh.read_settings"
    bl_label = "Read Settings"

    tool : StringProperty()

    def execute(self, context):
        readDefaultSettings(context, self.tool)
        return{'FINISHED'}

#----------------------------------------------------------
#  Init
#----------------------------------------------------------

def init():
    mhdir = getMHDirectory()

    bpy.types.Scene.MhProgramPath = StringProperty(
        name="MakeHuman Program Directory",
        description="Path to the MakeHuman program",
        maxlen=1024,
        default=mhdir
    )
    bpy.types.Scene.MhUserPath = StringProperty(
        name = "User Path",
        maxlen=1024,
        default=mhdir
    )
    bpy.types.Scene.MhTargetPath = StringProperty(
        name = "Target Path",
        default = os.path.join(mhdir, "data", "custom")
    )
    bpy.types.Scene.MhClothesDir = StringProperty(
        name="Directory",
        description="Path to the directory where clothes are stored",
        maxlen=1024,
        default=os.path.join(mhdir, "data", "clothes")
    )
    bpy.types.Scene.MhUvsDir = StringProperty(
        name="Directory",
        description="Path to the directory where UV sets are stored",
        maxlen=1024,
        default=os.path.join(mhdir, "data", "uvs")
    )

