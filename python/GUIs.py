"""
Created on 02.01.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript von Maya

"""

import maya.cmds as cmds
x_txt = cmds.intField
y_txt = cmds.intField
def InitUI():
    winID = "InitPos"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    # Create the window
    cmds.window(winID)

    # Master Layout
    masterLayout = cmds.columnLayout()

    # Platzhalter + Strich
    cmds.separator(style='none', height=16)
    cmds.separator(style='in', width=224)
    cmds.separator(style='none', height=16)

    # Laying out the rowColumnLayout is simple as this
    table1 = cmds.rowColumnLayout(numberOfColumns=7,
                                  columnWidth=[(1, 32), (2, 32), (3, 32), (4, 32), (5, 32), (6, 32), (7, 32)])

    cmds.separator(style='none', width=32)

    # Add first line of controls
    cmds.text(label="Reihe")
    x_txt = cmds.intField(minValue=1, maxValue=3)

    cmds.separator(style='none', width=32)

    # Adding more controls starts on the next row down.
    cmds.text(label="Spalte")
    y_txt = cmds.intField(minValue=1, maxValue=3)

    cmds.separator(style='none', width=32)

    # Wieder zurueck zum masterLayout
    cmds.setParent('..')

    cmds.separator(style='none', height=16)
    cmds.separator(style='in', width=224)
    cmds.separator(style='none', height=16)

    # Zweites TableLayout
    table2 = cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 32), (2, 64), (3, 32), (4, 64), (5, 32)])

    cmds.separator(style='none', width=32)
    cmds.button(label='Preview',
                command='r.setIniPos(cmds.intField(x_txt, query=True, value=True),cmds.intField(y_txt, query=True, value=True))')
    cmds.separator(style='none', width=32)
    cmds.button(label='Weiter')
    cmds.separator(style='none', width=32)

    # Wieder zurueck zum masterLayout
    cmds.setParent('..')

    cmds.separator(style='none', height=16)

    # show window
    cmds.showWindow(winID)

def AnimationUI():

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

    # Ein Layout fuer die Angabe der Sekunden zwischen den Keyframes
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

    # Layout fuer den Button
    table3 = cmds.rowColumnLayout( numberOfColumns=3, columnWidth=[ (1,100),(2,200),(3,100) ] )

    cmds.separator(style='none', width=100, height=25)
    cmds.button(label = 'Animationspunkt setzen', command = '')
    cmds.separator(style='none', width=100)

    cmds.setParent('..')

    # Zeigt das Fentser an
    cmds.showWindow(winID)