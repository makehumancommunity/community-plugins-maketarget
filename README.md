# MakeTarget 2

This repository contains a reimplementation of MakeTarget.

## Requirements

This version of the addon is blender 2.80 only. If you still use blender 2.79, you're better off using the previous 
version of MakeTarget. You can find the latest working version of the previous codebase in the "v1" branch in this repository.

Further, this version of the addon depends heavily on [the makehuman plugin for blender](https://github.com/makehumancommunity/makehuman-plugin-for-blender) or
[makeclothes plugin for blender](https://github.com/makehumancommunity/community-plugins-makeclothes).

In practise, you will need this in order to load a human mesh. The scale of the mesh is predefined by the makehuman plugin for blender - or - set to 1.0 when the mesh is loaded with makeclothes plugin.

The data is written as vertex-number, followed by x, y, z values. These values are rounded and have the same form as all the lines in uncompiled MakeHuman targets.

## Usage

When installed, you will find a "MakeTarget2" panel on the N-shelf in blender. 

The basic workflow is:

* Import a human mesh using the makehuman plugin for blender (see [this introductory video](https://www.youtube.com/watch?v=eEaVZVbTJOQ&t=101s) for more information). Make sure to *not* use a body proxy. 
* Select the body
* enter a name for your target
* Click "Initialize" in the make target panel. A shape key using the target name is created.
* Enter edit mode and model the target
* Exit edit mode
* Click "Save target" 



