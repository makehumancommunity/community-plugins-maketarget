#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras
import os
import bmesh
import math
from mathutils import Vector

class CRefVert:
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return ("<CRefVert %s\n    %s\n    %s>" % (self.verts, self.weights, self.offsets))

    def fromSingle(self, vn):
        self.verts = (vn,vn,vn)
        self.weights = (1,0,0)
        self.offsets = Vector((0,0,0))
        return self

    def fromTriple(self, verts, weights, offsets):
        self.verts = verts
        self.weights = weights
        self.offsets = Vector(offsets)
        return self

    def update(self, srcVerts):
        rv0,rv1,rv2 = self.verts
        w0,w1,w2 = self.weights
        return w0*srcVerts[rv0].co + w1*srcVerts[rv1].co + w2*srcVerts[rv2].co + self.offsets

    def updateWithScale(self, srcVerts, scales):
        rv0,rv1,rv2 = self.verts
        w0,w1,w2 = self.weights
        offset = [ self.offsets[n]*scales[n] for n in range(3) ]
        return w0*srcVerts[rv0].co + w1*srcVerts[rv1].co + w2*srcVerts[rv2].co + Vector(offset)

class Helper:
    def __init__(self):
        self.refVerts = {}
        self.xScale = None
        self.yScale = None
        self.zScale = None
        self.firstVert = 0

    def __str__(self):
        return (str(self.refVerts))

    def scaleInfo(self,words):
        v1 = int(words[1])
        v2 = int(words[2])
        den = float(words[3])
        return (v1, v2, den)

    def getScale(self, info, verts, index):
        if info is None:
            return 1.0
        (vn1, vn2, den) = info
        if index >= 0:
            num = abs(verts[vn1].co[index] - verts[vn2].co[index])
        else:
            v1 = verts[vn1].co
            v2 = verts[vn2].co
            dx = v1[0]-v2[0]
            dy = v1[1]-v2[1]
            dz = v1[2]-v2[2]
            num = math.sqrt(dx*dx + dy*dy + dz*dz)
        return num/den

    def getScales(self, verts):
        s0 = self.getScale(self.xScale, verts, 0)
        s2 = self.getScale(self.yScale, verts, 2)
        s1 = self.getScale(self.zScale, verts, 1)
        return ((s0, s1, s2))

    def modifyHelper(self, base, target, scale):
        first = self.firstVert
        if scale:
            scales = h.getScales(base)
            for n in range (0, len(self.refVerts)):
                target[n+first].co = self.refVerts[n].updateWithScale(target, scales)
        else:
            for n in range (0, len(self.refVerts)):
                target[n+first].co = self.refVerts[n].update(target)


    def readHelper(self, filepath):
        try:
            tmpl = open(filepath, "rU")
        except:
            return False

        status = 0
        doVerts = 1

        vn = 0
        scales = Vector((1.0, 1.0, 1.0))
        status = 0
        for line in tmpl:
            words= line.split()
            if len(words) == 0:
                continue
            key = words[0]
            if key[0] == '#':
                continue

            if key == 'verts':
                if len(words) > 1:
                    self.firstVert = int(words[1])
                status = doVerts
            elif key == 'x_scale':
                self.xScale = self.scaleInfo(words)
            elif key == 'y_scale':
                self.yScale = self.scaleInfo(words)
            elif key == 'z_scale':
                self.zScale = self.scaleInfo(words)

            elif status == doVerts:
                if len(words) == 1:
                    v = int(words[0])
                    self.refVerts[vn] = CRefVert(vn).fromSingle(v)
                else:
                    v0 = int(words[0])
                    v1 = int(words[1])
                    v2 = int(words[2])
                    w0 = float(words[3])
                    w1 = float(words[4])
                    w2 = float(words[5])
                    d0 = float(words[6])
                    d1 = float(words[7])
                    d2 = float(words[8])
                    self.refVerts[vn] = CRefVert(vn).fromTriple((v0,v1,v2), (w0,w1,w2), (d0,-d2,d1))
                vn += 1

        self.nverts = vn
        tmpl.close()
        return True

def _fixhelper(baseVerts, targetVerts):
    h = Helper()
    res = h.readHelper()
    if res is False:
        return False

    # modify with a scale of 1.0 (so false)
    #
    h.modifyHelper(base, target, False)

    return True

class MHC_OT_FixHelper(bpy.types.Operator):
    """Adapt helper to basemesh"""
    bl_idname = "mh_community.fix_helper"
    bl_label = "Adapt helper to basemesh"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if obj is not None:
            if not hasattr(obj, "MhObjectType"):
                return False
            if obj.select_get():
                if obj.MhObjectType == "Basemesh":
                    if obj.data.shape_keys and obj.data.shape_keys.key_blocks and obj.active_shape_key_index != 0:
                        return True
        return False

    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = context.active_object
        for mod in obj.modifiers:
            if mod.type == "MASK" and mod.name == "Hide Helper":
                mod.show_viewport = False

        sks = obj.data.shape_keys
        idx = obj.active_shape_key_index
        target = sks.key_blocks[idx].data
        base = sks.key_blocks[0].data
        filename = context.scene.MhHelperGeometry + ".mhclo"

        filepath = os.path.join(os.path.dirname(__file__), "data", filename)
        h = Helper()
        res = h.readHelper(filepath)
        if res is False:
            self.report({'ERROR'}, filename + " (proxy-weights) are missing")
            return {'CANCELLED'}

        # modify with a scale of 1.0 (so false)
        #
        h.modifyHelper(base, target, False)

        self.report({'INFO'}, "Adapt helper to base")
        return {'FINISHED'}

class MHC_OT_HideHelper(bpy.types.Operator):
    """Hide Helper"""
    bl_idname = "mh_community.hide_helper"
    bl_label = "Hide Helper"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        if not hasattr(obj, "MhObjectType"):
            return False
        if obj.MhObjectType != "Basemesh":
            return False
        return obj and obj.type == "MESH"

    def execute(self, context):
        obj = context.active_object

        if obj.mode == "EDIT":
            bpy.ops.mesh.select_mode(type="VERT")
            me = obj.data
            bm = bmesh.from_edit_mesh(me)
            for vert in bm.verts:
                vert.select = (vert.index >= 13380)         # this will not be hardcoded later
            bm.select_flush(True)
            bm.select_flush(False)

            bmesh.update_edit_mesh(me, destructive=False)

            bpy.ops.mesh.hide(unselected=False)
        else:
            for mod in obj.modifiers:
                if mod.type == "MASK" and mod.name == "Hide Helper":
                    mod.show_viewport = True
        return {'FINISHED'}

class MHC_OT_ShowHelper(bpy.types.Operator):
    """Show Helper"""
    bl_idname = "mh_community.show_helper"
    bl_label = "Show Helper"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(self, context):
        obj = context.active_object
        return obj and obj.type == "MESH"

    def execute(self, context):
        obj = context.active_object
        if obj.mode == "EDIT":
            bpy.ops.mesh.reveal()
        else:
            for mod in obj.modifiers:
                if mod.type == "MASK" and mod.name == "Hide Helper":
                    mod.show_viewport = False

        return {'FINISHED'}
