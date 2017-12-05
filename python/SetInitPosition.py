"""

"""

import maya.cmds as cmds
if not cmds.commandPort(':4434', q=True):
    cmds.commandPort(n=':4434')

class SetInitPosition():

    posX = 0
    posY = 0
    posZ = 0

    def __init__(self):
        posX = 0
        posY = 0
        posZ = 0


cmds.select('pCube1')
cmds.scale(10,2,12)
