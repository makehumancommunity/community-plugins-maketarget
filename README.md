# MakeTarget 2 for MakeHuman Version II

This repository contains a version of MakeTarget which is capable to work with MakeHuman Version I und also II.

## Requirements

This version is tested with blender version 4.5 LTS. There is a maketarget inside [the makehuman plugin for blender II](https://github.com/makehumancommunity/mpfb2), which can be used for MakeHuman Version 1 or for the hm08 mesh of Version 2.

This version of MakeTarget should be used for MakeHuman Version 2, especially for non-hm08 meshes.

To get a hm08 character you need to load it with [makeclothes plugin for blender] (https://github.com/makehumancommunity/community-plugins-makeclothes).

You can also assign a custom character or mesh (assign custom base), if you need symmetry there must be a mirror-file in the data folder of maketarget.

The scale of the mesh is set to 1.0 when the mesh is loaded with makeclothes plugin. For a custom mesh it would usually be 10 (especially when the .obj file was exported from Blender to Makehuman II).

The data is written as vertex-number, followed by x, y, z values. These values are rounded and have the same form as all the lines in uncompiled MakeHuman targets.

## Usage

_More detailed information will be on the MakeHuman page soon._

When installed, you will find a "MakeTarget2" panel on the N-shelf in blender. 

The basic workflow for hm08 mesh including helper is:

* Change to Makeclothes
* Import female-helper or male-helper with "import predefined human", do not use t-posed mesh. Makeclothes sets character mesh-type to hm08 and uses scale 1.0.
* Change to Maketarget II
* Enter a name for your target
* Click "Add a new target" in the make target panel. A shape key using the target name is created. Mesh is displayed without helper.
* Enter edit mode and model the target (hide helper just to model the body)
* Exit edit mode
* Change helper if needed, do it manually or use the automatic function. For automatic function select type of helper, so either male or female for standard pose and press "Adapt helper mesh to base". Usually some additional work is needed.
* Click "Save target" 


The basic workflow for a different mesh (custom base) is:

* import obj file or load file with the standard base
* Set scale. If the file is the unchanged base for MakeHuman II, it would be normally 10.
* Assign the base. System will detect if a mirror table in the data directory of maketarget with that name is available, currently available are hm08 and mh2bot.
* Enter a name for your target
* Click "Add a new target" in the make target panel. A shape key using the target name is created.
* Enter edit mode and model the target.
* Exit edit mode
* Click "Save target" 

