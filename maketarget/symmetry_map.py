import re
import os

def MirrorByTable(obj, pt, direction):

    MirrorTable = {}

    meshtype = "hm08"                   # preset mesh  name
    if hasattr (obj, "MhMeshType"):
        meshtype = obj.MhMeshType

    mirrorfilename =  meshtype + ".mirror"
    mirrorfile = os.path.join(os.path.dirname(__file__), "data", mirrorfilename)
    try:
        f = open(mirrorfile)
        for line in f:
            m=re.search("(\d+)\s+(\d+)\s+(\w+)", line)
            if (m is not None):
                MirrorTable[int (m.group(1))] = { 'm': int(m.group(2)), 's': m.group(3) }
        f.close()
    except IOError:
        return False, mirrorfilename

    for idx, source in enumerate (pt):
        if MirrorTable[idx]['s'] == direction:
            dest = pt[MirrorTable[idx]['m']]
            dest.co[0] = -source.co[0]
            dest.co[1] = source.co[1]
            dest.co[2] = source.co[2]
        elif MirrorTable[idx]['s'] == 'm':
            source.co[0] = 0

    return True, mirrorfilename

