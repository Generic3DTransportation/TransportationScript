"""
Created on 02.01.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript von Maya

"""

import maya.cmds as cmds

def UI():

    # Loescht Fenster, wenn das Fenster davor schon offen war
    winID = "Animation"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    # Erzeugt ein leeres Fenster
    animationWindow = cmds.window("Animation", title = "Animation erzeugen", h = 100, w = 400, sizeable = False)

    # Layout erstellen
    mainLayout = cmds.columnLayout(w = 400, h = 200)
    cmds.separator(style='none', height=25)

    # Rows fuer die einzelnen Motoren
    row1mot = cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180) ] )

    cmds.separator(style='none', width=50, height=15)
    cmds.text(label="Motor 1")
    cmds.separator(style = 'none', width = 10)
    motor1 = cmds.intField(minValue = 0, maxValue = 180)
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(0 - 180 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row2mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 2")
    cmds.separator(style='none', width=10)
    motor2 = cmds.intField(minValue=0, maxValue=180)
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(0 - 180 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row3mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 3")
    cmds.separator(style='none', width=10)
    motor3 = cmds.intField(minValue=0, maxValue=180)
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(0 - 180 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row4mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 4")
    cmds.separator(style='none', width=10)
    motor4 = cmds.intField(minValue=0, maxValue=180)
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(0 - 180 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row5mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 5")
    cmds.separator(style='none', width=10)
    motor5 = cmds.intField(minValue=0, maxValue=180)
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(0 - 180 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    cmds.setParent('..')

    # Ein Layout für die Angabe der Sekunden zwischen den Keyframes
    table2 = cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180) ] )

    cmds.separator(style='none', width=50)
    cmds.text(label="Animationsabstand")
    cmds.separator(style='none', width=10)
    motor1 = cmds.intField(minValue=0, maxValue=25)
    cmds.separator(style='none', width=10)
    cmds.text(label="sec")
    cmds.text(label="(0 - 25 Sekunden)")
    cmds.separator(style='none', height=25)

    cmds.setParent('..')

    # Layout für den Button
    table3 = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,100),(2,200),(3,100) ] )

    cmds.separator(style='none', width=100, height=25)
    cmds.button(label = 'Animationspunkt setzen', command = '')
    cmds.separator(style='none', width=100)

    cmds.setParent('..')

    # Zeigt das Fentser an
    cmds.showWindow(AnimationWindow)