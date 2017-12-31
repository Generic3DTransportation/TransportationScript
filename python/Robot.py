"""
Created on 05.12.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript von Maya

"""

import maya.cmds as cmds

init_pos = [
    [
        ( 24.2208673777 , -41.0184917399 , 46.5470565213 , 99.6468447193 , 24.3908459759), #1,1
        ( 0.0           , -29.5138730516 , 29.8171860725 , 0.0           , 0.0          ), #1,2
        (-24.5006994327 , -38.3159782227 , 43.2466070017 , 82.3092736792 , -24.9212142879) #1,3
    ],[
        ( 24.2542695286 , -48.5850473953 , 24.2467577445 , 47.1088280626 , 34.8416390552), #2,1
        ( 0.0           , -39.9816170921 , 8.33797300612 , 0.0           , 31.7120945831), #2,2
        (-24.2026573146 , -49.3625765099 , 24.9155083418 , -46.3835349099, 33.7064322236)  #2,3
    ],[
        ( 24.4124390804 , -72.1272022546 , 28.3597634909 , 33.4458530711 , 49.0086665745), #3,1
        ( 0.0           , -65.5428306502 , 12.4581533675 , 0.0           , 53.1341838858), #3,2
        (-24.2227667207 , -72.227931493  , 29.0615864173 , -33.0532596406, 48.5914699938)  #3,3
    ]
]

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

    def setIniPos(self,x,y):
        w = init_pos[x-1][y-1]
        self.update1(w[0])
        self.update2(w[1])
        self.update3(w[2])
        self.update4(w[3])
        self.update5(w[4])

#tests

r = Robot()
# w = init_pos[0][2]
# r.a1=w[0]
# r.a2=w[1]
# r.a3=w[2]
# r.a4=w[3]
# r.a5=w[4]
# r.updateAll()
# print("1: "+str(cmds.getAttr('achse1.rotateY')))
# print("2: "+str(cmds.getAttr('achse2.rotateZ')))
# print("3: "+str(cmds.getAttr('achse3.rotateZ')))
# print("4: "+str(cmds.getAttr('achse4.rotateX')))
# print("5: "+str(cmds.getAttr('achse5.rotateZ')))

winID = "InitPos"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

# Create the window
cmds.window(winID)

# Master Layout
masterLayout = cmds.columnLayout()

# Platzhalter + Strich
cmds.separator (style='none', height=16)
cmds.separator( style='in', width=224)
cmds.separator (style='none', height=16)

# Laying out the rowColumnLayout is simple as this
table1 = cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[ (1,32),(2,32),(3,32),(4,32),(5,32),(6,32),(7,32) ] )

cmds.separator (style='none', width=32)

# Add first line of controls
cmds.text( label="Reihe" )
x_txt = cmds.intField(minValue=1, maxValue=3)

cmds.separator (style='none', width=32)

# Adding more controls starts on the next row down.
cmds.text( label="Spalte" )
y_txt = cmds.intField(minValue=1, maxValue=3)

cmds.separator (style='none', width=32)

# Wieder zurück zum masterLayout
cmds.setParent('..')

cmds.separator (style='none', height=16)
cmds.separator( style='in', width=224)
cmds.separator (style='none', height=16)

# Zweites TableLayout
table2 = cmds.rowColumnLayout( numberOfColumns=5, columnWidth=[ (1,32),(2,64),(3,32),(4,64),(5,32) ] )

cmds.separator (style='none', width=32)
cmds.button(label='Preview', command='r.setIniPos(cmds.intField(x_txt, query=True, value=True),cmds.intField(y_txt, query=True, value=True))')
cmds.separator (style='none', width=32)
cmds.button(label='Weiter')
cmds.separator (style='none', width=32)

# Wieder zurück zum masterLayout
cmds.setParent('..')

cmds.separator (style='none', height=16)

# show window
cmds.showWindow(winID)