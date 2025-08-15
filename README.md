# MakeTarget 2 for MakeHuman Version II

This repository contains a version of MakeTarget which is capable to work with MakeHuman Version I und also II.

## Requirements

This version is tested with blender version 4.5 LTS. There is a maketarget inside [the makehuman plugin for blender II](https://github.com/makehumancommunity/mpfb2), which can be used for MakeHuman Version 1 oder for the hm08 mesh of Version 2.

This version of MakeTarget should be used for MakeHuman Version 2, especially for non-hm08 meshes.

To get a hm08 character you need to load [makeclothes plugin for blender] as well (https://github.com/makehumancommunity/community-plugins-makeclothes).

You can also assign a custom character or mesh (assign custom base), be aware you need a mirror file for this base in the data folder of maketarget.
At the moment we assume symmetric characters.

The scale of the mesh is set to 1.0 when the mesh is loaded with makeclothes plugin. For a custom mesh it could usually be 10 (when the .obj file was exported from Blender to Makehuman II.

The data is written as vertex-number, followed by x, y, z values. These values are rounded and have the same form as all the lines in uncompiled MakeHuman targets.

## Usage

More detailed information will be on the MakeHuman page soon.

When installed, you will find a "MakeTarget2" panel on the N-shelf in blender. 

The basic workflow for hm08 mesh including helper is:

* Change to Makeclothes
* Import female-helper or male-helper (import predefined human), do not use t-posed mesh. Makeclothes sets character mesh-type to hm08 and uses scale 1.0.
* Change to Maketarget II
* Enter a name for your target
* Click "Add a new target" in the make target panel. A shape key using the target name is created. Mesh is displayed without helper.
* Enter edit mode and model the target (hide helper just to model the body)
* Exit edit mode
* Change the helper of hm08 mesh, select type of helper, so either male or female for standard pose.
* Adapt helper mesh to base
* Click "Save target" 


The basic workflow for a different mesh (custom base) is:

* import obj file or load file with the standard base
* Set scale. If the file is the unchanged base for MakeHuman II, it would be normally 10.
* Assign the base (a mirror table in the data directory of maketarget with that name should be available, currently available are hm08 and mh2bot)
* Enter a name for your target
* Click "Add a new target" in the make target panel. A shape key using the target name is created.
* Enter edit mode and model the target.
* Exit edit mode
* Click "Save target" 

