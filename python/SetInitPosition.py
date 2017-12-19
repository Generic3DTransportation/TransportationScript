"""
Created on 05.12.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript von Maya

"""

import maya.cmds as cmds

class Robot():

    def __init__(self):
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0
        self.a4 = 0
        self.a5 = 0

    def updateAll(self):
        self.update1(self.a1)
        self.update2(self.a2)
        self.update3(self.a3)
        self.update4(self.a4)
        self.update5(self.a5)

    def update1(self, achse1):
        cmds.select('achse1')
        cmds.rotate(0, achse1, 0)

    def update2(self, achse2):
        cmds.select('achse2')
        cmds.rotate(0, 0, achse2)

    def update3(self, achse3):
        cmds.select('achse3')
        cmds.rotate(0, 0, achse3)

    def update4(self, achse4):
        cmds.select('achse4')
        cmds.rotate(achse4, 0, 0)

    def update5(self, achse5):
        cmds.select('achse5')
        cmds.rotate(0, 0, achse5)

    def createIniGUI(self):
        cmds.window(title="Setup Starting Point")
        cmds.columnLayout()
        cmds.textField()
#tests

r = Robot()
r.a1=40
r.a3=50
r.updateAll()
print(cmds.getAttr('achse1.rotateY'))