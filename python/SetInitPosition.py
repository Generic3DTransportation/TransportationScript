"""
Created on 05.12.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript von Maya

"""

import maya.cmds as cmds

class SetInitPosition():

    posX = 0
    posY = 0
    posZ = 0

    def __init__(self):
        posX = 0
        posY = 0
        posZ = 0

#tests
cmds.select('achse01')
cmds.rotate(0, '125deg', 0)
