#!/usr/bin/python
# -*- coding: ascii -*-
"""
Created on 05.12.2017

@author: Michael Ostrowski <mostrowski@student.tgm.ac.at>, Michael Frank <mfrank01@student.tgm.ac.at>
@version: 20170512

@description: Pythonscript fuer Roboteransteuerung
"""
import maya.cmds as cmds
import os
import time

# Die Winkelpositionen des Roboters fuer die Anfangsposition, um das Paket zu nehmen
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
# Maximale Geschwindigkeit der Achsen (in Grad pro Sekunde)
max_speed = (105, 107, 114, 179, 172)
# Fuellt die Animation ueber das A4 Blatt aus
fill_animation = (27.5, 55/3/2, -55/3/2, -27.5)
class Robot():
    """
    Das Roboterobjekt, welches fuer die direkte Ansteuerung
    des einzelen Roboterarms zustaendig ist.
    """

    def __init__(self, name):
        """
        Die Initialisierung des Roboterobjekts.
        :param name: Der vergebene Name des Roboterarms in Maya, um diesen anzusteuern.
        """
        # Achsenname ist der eindeutige Name, mit dem jede Achse jedes Roboterarms angesteuert wird.
        self.achsname1 = name + "|achse1"
        self.achsname2 = name + "|achse1|achse2"
        self.achsname3 = name + "|achse1|achse2|achse3"
        self.achsname4 = name + "|achse1|achse2|achse3|achse4"
        self.achsname5 = name + "|achse1|achse2|achse3|achse4|achse5"

        # Der Winkel jeder Achse
        self.a1 = 0
        self.a2 = 0
        self.a3 = 0
        self.a4 = 0
        self.a5 = 0

        # Die Laenge der Animation
        self.totalpasttime = 0

        # Paket welches der Roboter transportiert
        self.package = 0,0

    def updateAll(self):
        """
        Aktualisiert alle Winkel des Roboterarms nach den gesetzten Winkel des Roboterobjekts
        """
        self.setAchse1(self.a1)
        self.setAchse2(self.a2)
        self.setAchse3(self.a3)
        self.setAchse4(self.a4)
        self.setAchse5(self.a5)

    # Methoden zu setzen der einzelnen Achsen des Roboterarms
    def setAchse1(self, achse1):
        cmds.select(self.achsname1)
        cmds.rotate(0, achse1, 0)

    def setAchse2(self, achse2):
        cmds.select(self.achsname2)
        cmds.rotate(0, 0, achse2)

    def setAchse3(self, achse3):
        cmds.select(self.achsname3)
        cmds.rotate(0, 0, achse3)

    def setAchse4(self, achse4):
        cmds.select(self.achsname4)
        cmds.rotate(achse4, 0, 0)

    def setAchse5(self, achse5):
        cmds.select(self.achsname5)
        cmds.rotate(0, 0, achse5)

    def setIniPos(self,x,y):
        """
        Setzt die Position des Roboterarms neben dem gewaehlten Paket im Regal.
        :param x: Die Reihe im Regal
        :param y: Die Spalte im Regal
        """
        w = init_pos[x-1][y-1]
        self.setAchse1(w[0])
        self.setAchse2(w[1])
        self.setAchse3(w[2])
        self.setAchse4(w[3])
        self.setAchse5(w[4])

    def getMotorRotation(self,time):
        """
        Gibt eine Liste an Winkeln der jeweiligen Motoren auf Sekunde 'time' zurueck.
        :param time: Die Sekunde in der Animation
        :return: Eine Liste an Winkeln der einzelnen Motoren
        """
        # Setzt die Zeit in der Animation
        cmds.currentTime(str(time) + 'sec', edit=True)
        RotationList = []
        RotationList.append(cmds.getAttr(self.achsname1+'.rotateY'))
        RotationList.append(cmds.getAttr(self.achsname2+'.rotateZ'))
        RotationList.append(cmds.getAttr(self.achsname3+'.rotateZ'))
        RotationList.append(cmds.getAttr(self.achsname4+'.rotateX'))
        RotationList.append(cmds.getAttr(self.achsname5+'.rotateZ'))
        return RotationList

    def attachPackage(self,x,y):
        """
        'Heftet' das Paket an den Roboterarm an, um es mit dem Roboterarm zu bewegen.
        :param x: Die Reihe im Regal
        :param y: Die Spalte im Regal
        """
        self.package = x,y
        # parent verschiebt ein Objekt in eine Gruppe.
        cmds.parent('p'+str(x)+str(y), self.achsname5)

    def setKeyframe(self,nexttime):
        """
        Setzt einen Keyframe in der Animation
        :param nexttime: Die Zeit zwischen letzten Keyframe und dem zu setzendem Keyframe
        """
        time = self.totalpasttime + nexttime
        self.totalpasttime += nexttime
        # Setzt Keyframe an allen Achsen
        cmds.setKeyframe(self.achsname1, at='rotateY', t=str(time) + 'sec')
        cmds.setKeyframe(self.achsname2, at='rotateZ', t=str(time) + 'sec')
        cmds.setKeyframe(self.achsname3, at='rotateZ', t=str(time) + 'sec')
        cmds.setKeyframe(self.achsname4, at='rotateX', t=str(time) + 'sec')
        cmds.setKeyframe(self.achsname5, at='rotateZ', t=str(time) + 'sec')
        # Validierung des Keyframes, ob ein Motor sich nicht zu schnell dreht.
        try:
            self.checkKeyframe(self.totalpasttime-nexttime, self.totalpasttime)
        except ValueError as err:
            SpeedUI(err.args[0])
            self.deleteKeyframe(self.totalpasttime)
            self.totalpasttime -= nexttime
            cmds.currentTime(str(self.totalpasttime) + 'sec', edit=True)

    def checkKeyframe(self, lastTime, nextTime):
        """
        # Validierung des Keyframes, ob ein Motor sich nicht zu schnell dreht.
        :param lastTime: Der Zeitpunkt des letzten Keyframes
        :param nextTime: Der Zeitpunkt des zu setzendem Keyframes
        """
        if nextTime - lastTime > 0:
            # Listen der Motorenwinkel zu den Zeitpunkten des Keyframes
            lastRotation = self.getMotorRotation(lastTime)
            nextRotation = self.getMotorRotation(nextTime)
            for i in range(5):
                # print(str(abs(nextRotation[i]-lastRotation[i]))+" durch "+str(nextTime-lastTime)+" ist "+str(max_speed[i]))
                # Lineare Berechnung der geschwindigkeit, obwohl logistische Animationskurve
                # TODO: logistische Berechnung der Geschwindigkeit der Motoren
                if abs(nextRotation[i]-lastRotation[i]) != 0 and (abs(nextRotation[i]-lastRotation[i])/(nextTime-lastTime)) > max_speed[i]:
                    raise ValueError("Rotation bei Motor "+str(i+1)+ " ist zu schnell!")

    def deleteKeyframe(self, time):
        """
        Loescht einen Keyframe in der Animation
        :param time: die Sekunde des Keyframes
        """
        # Eine Liste aller Objekte in Maya
        selectAll = cmds.ls()
        # Loeschen des Keyframes
        cmds.cutKey(selectAll, t=(str(time)+'sec',str(time)+'sec'))

def newRobot(name):
    """
    Erstellt einen neuen Roboterarm
    :param name: Bezeichnung des neuen Roboterarms
    :return: Das Roboterobjekt
    """
    cmds.duplicate('Robot', n=name)
    return Robot(name)

def printManualAnimation():
    """
    Exportierung der Animierung in ein externes File mit 4 Zeitpunkten graphisch gargestellt.
    """
    # Create File
    # cmds.file(f=True, new=True)
    timeseg = float(r.totalpasttime)/3

    # Erstellung von 4 Roboterarmen an den 4 Zeitpunkten der Animation
    cmds.currentTime('0sec', edit=True)
    r1 = newRobot("r1")
    cmds.currentTime(str(timeseg) + 'sec', edit=True)
    r2 = newRobot("r2")
    cmds.currentTime(str(timeseg * 2) + 'sec', edit=True)
    r3 = newRobot("r3")
    cmds.currentTime(str(r.totalpasttime) + 'sec', edit=True)
    r4 = newRobot("r4")

    # Speichern der Dauer der Animation
    with open("time_manual.conf","w+") as f:
        f.write(str(r.totalpasttime))

    # Kopieren von Regal, Tisch und Platte zum Export in das File
    cmds.duplicate('Regal', n='Regal_Frame')
    cmds.duplicate('Tisch', n='Tisch_Frame')
    cmds.duplicate('Platte', n='Platte_Frame')

    # Selektion aller Objekte welche exportiert werden sollen
    # und Verschiebung der Roboterarme auf die zeitlich proportionalen Positionen
    cmds.select('Regal_Frame', r=True)
    cmds.select('r1', add=True)
    cmds.move(fill_animation[0], moveX=True, relative=True)
    cmds.select('Tisch_Frame', r=True)
    cmds.select('r4', add=True)
    cmds.move(fill_animation[3], moveX=True, relative=True)
    cmds.select('r2', r=True)
    cmds.move(fill_animation[1], moveX=True, relative=True)
    cmds.select('r3', r=True)
    cmds.move(fill_animation[2], moveX=True, relative=True)
    cmds.select('Platte_Frame', r=True)
    cmds.select('Tisch_Frame', add=True)
    cmds.select('Regal_Frame', add=True)
    cmds.select('r1', add=True)
    cmds.select('r2', add=True)
    cmds.select('r3', add=True)
    cmds.select('r4', add=True)
    cmds.move(-5, moveZ=True, relative=True)

    # Export der Selektion in PrintRobot.mb
    cmds.file(os.getcwd()+'/PrintRobot_manual.mb', type='mayaBinary', exportSelected=True)
    # Selektion wird nach Export geloescht
    cmds.delete()
    SpeedUI("Export abgeschlossen!")

def printAlgorithmAnimation(step):
    # Step 1 Animation "Aus dem Regal bewegen"
    if step == 1:
        before_rotate = r.getMotorRotation(0)
        # Paket wird aus dem Regal bewegt
        for i in range(0,4):
            if r.package[0] == 1:
                if r.package[1] == 2:
                    cmds.move(-.3, 0, 0, 'ikHandle', relative=True)
                else:
                    cmds.move(-.5, 1, 0, 'ikHandle', relative=True)
            else:
                if r.package[1] == 2:
                    cmds.move(-.3, .25, 0, 'ikHandle', relative=True)
                else:
                    cmds.move(-.5, .4, 0, 'ikHandle', relative=True)
        after_rotate = r.getMotorRotation(0)
        # Schnellst moegliche Zeit fuer diese Bewegung wird berechnet
        min_time = max(abs(before_rotate[1] - after_rotate[1]) / max_speed[1],
                       abs(before_rotate[2] - after_rotate[2]) / max_speed[2],
                       abs(before_rotate[3] - after_rotate[3]) / max_speed[3],
                       abs(before_rotate[4] - after_rotate[4]) / max_speed[4])
        # Mit schnellst moeglicher Zeit wird der Roboterarm bewegt
        cmds.setKeyframe(r.achsname1, at='rotateY', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname2, at='rotateZ', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname3, at='rotateZ', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname4, at='rotateX', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname5, at='rotateZ', t=str(min_time) + 'sec')
        r.totalpasttime += min_time
        cmds.currentTime(str(r.totalpasttime) + 'sec', edit=True)
    # Step 2 Animation "Zur Ausgabe rotieren"
    if step == 2:
        rest1 = 0
        if cmds.getAttr('achse1.rotateY') < 0:
            rest1 = -(-180 - cmds.getAttr('achse1.rotateY'))
            r.setAchse1(-180)
        else:
            rest1 = 180 - cmds.getAttr('achse1.rotateY')
            r.setAchse1(180)
        rest1_sek = float(rest1)/max_speed[0]
        cmds.setKeyframe(r.achsname1, at='rotateY', t=str(rest1_sek) + 'sec')
        cmds.setKeyframe(r.achsname2, at='rotateZ', t=str(r.totalpasttime+.3) + 'sec')
        cmds.setKeyframe(r.achsname3, at='rotateZ', t=str(r.totalpasttime+.3) + 'sec')
        cmds.setKeyframe(r.achsname4, at='rotateX', t=str(r.totalpasttime+.3) + 'sec')
        cmds.setKeyframe(r.achsname5, at='rotateZ', t=str(r.totalpasttime+.3) + 'sec')
        cmds.delete('ikHandle')
        cmds.currentTime(str(r.totalpasttime + rest1_sek) + 'sec', edit=True)
        # Speicherung wie lange die gesamte Animation dauert
        with open("time_algorithm.conf","w+") as f:
            f.write(str(r.totalpasttime + rest1_sek))
    # Step 3 Animation "Fuer die Ausgabe rotieren/positionieren"
    if step == 3:
        before_rotate = [cmds.getAttr('achse2.rotateZ'),cmds.getAttr('achse3.rotateZ'),cmds.getAttr('achse4.rotateX'),cmds.getAttr('achse5.rotateZ')]
        after_rotate = [-52.2985745581, 34.7935752632, 0.0, -74.1268957397]
        r.setAchse2(after_rotate[0])
        r.setAchse3(after_rotate[1])
        r.setAchse4(after_rotate[2])
        r.setAchse5(after_rotate[3])
        min_time = max(abs(before_rotate[0] - after_rotate[0]) / max_speed[1],
                       abs(before_rotate[1] - after_rotate[1]) / max_speed[2],
                       abs(before_rotate[2] - after_rotate[2]) / max_speed[3],
                       abs(before_rotate[3] - after_rotate[3]) / max_speed[4])
        min_time += r.totalpasttime
        # Mit schnellst moeglicher Zeit wird der Roboterarm bewegt
        cmds.setKeyframe(r.achsname2, at='rotateZ', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname3, at='rotateZ', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname4, at='rotateX', t=str(min_time) + 'sec')
        cmds.setKeyframe(r.achsname5, at='rotateZ', t=str(min_time) + 'sec')
    # Step 4 Export Animation for printing
    if step == 4:
        timeproportion = 1
        isCombined = False
        with open("time_algorithm.conf", "r") as f:
            algorithm_animation_time = float(f.read())
        try:
            with open("time_manual.conf", "r") as f:
                manual_animation_time = float(f.read())
            timeproportion = algorithm_animation_time / manual_animation_time
            isCombined = True
        except:
            SpeedUI("Kombinierung nicht m?glich!")

        timeseg = float(algorithm_animation_time) / 3

        # Erstellung von 4 Roboterarmen an den 4 Zeitpunkten der Animation
        cmds.currentTime('0sec', edit=True)
        r1 = newRobot("r1_alg")
        cmds.currentTime(str(timeseg) + 'sec', edit=True)
        r2 = newRobot("r2_alg")
        cmds.currentTime(str(timeseg * 2) + 'sec', edit=True)
        r3 = newRobot("r3_alg")
        cmds.currentTime(str(algorithm_animation_time) + 'sec', edit=True)
        r4 = newRobot("r4_alg")

        # Kopieren von Regal, Tisch und Platte zum Export in das File
        cmds.duplicate('Regal', n='Regal_alg')
        cmds.duplicate('Tisch', n='Tisch_alg')
        cmds.duplicate('Platte', n='Platte_alg')

        # Selektion aller Objekte welche exportiert werden sollen
        # und Verschiebung der Roboterarme auf die zeitlich proportionalen Positionen
        cmds.select('Regal_alg', r=True)
        cmds.select('r1_alg', add=True)
        cmds.move(fill_animation[0]*timeproportion, moveX=True, relative=True)
        cmds.select('Tisch_alg', r=True)
        cmds.select('r4_alg', add=True)
        cmds.move(fill_animation[3]*timeproportion, moveX=True, relative=True)
        cmds.select('r2_alg', r=True)
        cmds.move(fill_animation[1]*timeproportion, moveX=True, relative=True)
        cmds.select('r3_alg', r=True)
        cmds.move(fill_animation[2]*timeproportion, moveX=True, relative=True)
        cmds.select('Platte_alg', r=True)
        cmds.select('Tisch_alg', add=True)
        cmds.select('Regal_alg', add=True)
        cmds.select('r1_alg', add=True)
        cmds.select('r2_alg', add=True)
        cmds.select('r3_alg', add=True)
        cmds.select('r4_alg', add=True)
        # Kombiniert den Manuellen und den algorithmischen Weg
        if isCombined:
            cmds.move(5, moveZ=True, relative=True)
            cmds.file(os.getcwd()+'/PrintRobot_manual.mb', i=True, f=True)
            cmds.select('Tisch_Frame', r=True)
            cmds.select('Regal_Frame', add=True)
            cmds.select('r1', add=True)
            cmds.select('r2', add=True)
            cmds.select('r3', add=True)
            cmds.select('r4', add=True)
            cmds.move(-5, moveZ=True, relative=True)

            cmds.select('Platte_Frame', add=True)
            cmds.select('Tisch_alg', add=True)
            cmds.select('Regal_alg', add=True)
            cmds.select('r1_alg', add=True)
            cmds.select('r2_alg', add=True)
            cmds.select('r3_alg', add=True)
            cmds.select('r4_alg', add=True)
        # Export der Selektion in PrintRobot.mb
        cmds.file(os.getcwd() + '/PrintRobot_algorithm.mb', type='mayaBinary', exportSelected=True)
        # Selektion wird nach Export geloescht
        cmds.delete()
        SpeedUI("Export abgeschlossen!")


# GUIs

def AnimationmodelUI():
    """
    Erstellung der GUI fuer die Auswahl der Startposition des Roboterarms auf ein Paket im Regal
    """
    winID = "Animationsmodel"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    # Create the window
    cmds.window("Animationsmodel", title="Auswahl des Animationmodels", h=150, w=400, sizeable=False)

    # Layout erstellen
    mainLayout = cmds.columnLayout(w=400, h=150)

    # # Platzhalter + Strich
    cmds.separator(style='none', width=50, height=15)

    # Laying out the rowColumnLayout
    table1 = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 10), (2, 380), (3, 10)])

    cmds.separator(style='none', width=50)
    cmds.text("Waehlen sie die Methode aus welcher die Animation herzustellen ist")
    cmds.separator(style='none', width=50)
    # Zurueck zum Hauptlayout
    cmds.setParent('..')

    cmds.separator(style='none', width=50, height=15)

    # Laying out secound rowColumnLayout
    table2 = cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 80), (2, 100), (3, 40), (4, 100), (5, 80)])

    cmds.separator(style='none', width=80)
    DirectionControl = cmds.radioCollection()
    Direction0 = cmds.radioButton(label='Manuell')
    cmds.separator(style='none', width=40)
    Direction1 = cmds.radioButton(label='Algorithmisch')
    cmds.separator(style='none', width=80)
    # Zurueck zum Hauptlayout
    cmds.setParent('..')

    cmds.separator(style='none', width=50, height=20)
    DirectionControl = cmds.radioCollection(DirectionControl, edit=True, select=Direction1)

    # Laying out the rowColumnLayout
    table1 = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 10), (2, 380), (3, 10)])

    def weiter(*_):
        """
        Wird man in die AnimationsGUI weitergefuehrt die man ausgewaehlt hat
        :param _: metadata des button Commands
        """
        radioCol = cmds.radioCollection(DirectionControl, query=True, sl=True)
        getSelectRadioVal = cmds.radioButton(radioCol, query=True, label=True)
        positionUI(getSelectRadioVal)

        # Schliesst die Init GUI
        cmds.deleteUI(winID)

    cmds.separator(style='none', width=50)
    cmds.button(label='Weiter', command=weiter)
    cmds.separator(style='none', width=50)
    # Zurueck zum Hauptlayout
    cmds.setParent('..')

    cmds.showWindow(winID)


def positionUI(selectedRadioVal):
    """
    Fenster dass zwischen Haendischer oder durch einen Algorightmus die Animation erstellt werden soll
    :param x: Die Reihe im Regal
    :param y: Die Spalte im Regal
    """
    winID = "positionUI"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    # Fenster erstellen
    cmds.window("positionUI", title="Auswahl des Regals", h=150, w=223, sizeable=False)

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
    x_txt = cmds.intField(minValue=1, maxValue=3, value=1)

    cmds.separator(style='none', width=32)

    # Adding more controls starts on the next row down.
    cmds.text(label="Spalte")
    y_txt = cmds.intField(minValue=1, maxValue=3, value=1)

    cmds.separator(style='none', width=32)

    # Wieder zurueck zum masterLayout
    cmds.setParent('..')

    cmds.separator(style='none', height=16)
    cmds.separator(style='in', width=224)
    cmds.separator(style='none', height=16)

    # Zweites TableLayout
    table2 = cmds.rowColumnLayout(numberOfColumns=5, columnWidth=[(1, 32), (2, 64), (3, 32), (4, 64), (5, 32)])

    cmds.separator(style='none', width=32)

    def setPos(*_):
        """
        Setzt die Anfangsposition des Roboterarms
        :param _: metadata des button Commands
        """
        r.setIniPos(cmds.intField(x_txt, query=True, value=True), cmds.intField(y_txt, query=True, value=True))

    cmds.button(label='Preview', command=setPos)
    cmds.separator(style='none', width=32)

    def weiter(*_):
        """
        Hier wird man in die Animations GUI weitergefuehrt
        :param _: metadata des button Commands
        """
        setPos(*_)
        r.attachPackage(cmds.intField(x_txt, query=True, value=True), cmds.intField(y_txt, query=True, value=True))
        # Setz den ersten Keyframe
        r.setKeyframe(0)
        if selectedRadioVal == "Manuell":
            AnimationUI(cmds.intField(x_txt, query=True, value=True), cmds.intField(y_txt, query=True, value=True))
        else:
            AlgorithmhUi(cmds.intField(x_txt, query=True, value=True), cmds.intField(y_txt, query=True, value=True))
        # Schliesst die Init GUI
        cmds.deleteUI(winID)

    cmds.button(label='Weiter', command=weiter)
    cmds.separator(style='none', width=32)

    # Wieder zurueck zum masterLayout
    cmds.setParent('..')

    cmds.separator(style='none', height=16)

    # show window
    cmds.showWindow(winID)

#Eventuell Parameter veraendern
def AlgorithmhUi(x,y):
    """
    Algorithmus Windows zum erstellen der Animation
    :param x: Die Reihe im Regal
    :param y: Die Spalte im Regal
    """
    winID = "AlgorithmUI"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)
    # Create the window
    algorithmWindow = cmds.window("AlgorithmUI", title="Animation erzeugen", h=200, w=400, sizeable=False)


    # Layout erstellen
    mainLayout = cmds.columnLayout(w=400, h=200)
    # TODO: Inhalt fuellen
    cmds.separator(style='none', height=25)

    # Laying out the rowColumnLayout
    table1 = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 10), (2, 380), (3, 10)])

    cmds.separator(style='none', width=10)
    maxvalue = 4
    progressControl = cmds.progressBar(maxValue=maxvalue, width=380)
    cmds.separator(style='none', width=10)
    cmds.setParent('..')

    # To see Progress in % on ProgressBar
    cmds.progressBar(progressControl, edit=True, step=1)
    cmds.separator(style='none', width=50, height=15)

    # TODO: Fill code, change with actual Code
    table3 = cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 100), (2, 200), (3, 100)])
    cmds.separator(style='none', width=10)
    def test(*_):
        for i in range(1, maxvalue+1):
            if(i == 1):
                cmds.progressBar(progressControl, edit=True, step=1)
                printAlgorithmAnimation(1)
            elif(i == 2):
                cmds.progressBar(progressControl, edit=True, step=1)
                printAlgorithmAnimation(2)
            elif (i == 3):
                cmds.progressBar(progressControl, edit=True, step=1)
                printAlgorithmAnimation(3)
            elif (i == 4):
                cmds.progressBar(progressControl, edit=True, step=1)
                printAlgorithmAnimation(4)
    cmds.button(label='Starte Algorithmus', command=test, width=200)
    cmds.separator(style='none', width=10)
    cmds.setParent('..')

    cmds.showWindow(winID)


def AnimationUI(x,y):
    """
    Die GUI fuer die Animation des Roboterarms
    :param x: Die Reihe im Regal
    :param y: Die Spalte im Regal
    """

    # Loescht Fenster, wenn das Fenster davor schon offen war
    winID = "Animation"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)

    # Erzeugt ein leeres Fenster
    animationWindow = cmds.window("Animation", title="Animation erzeugen", h=375, w=400, sizeable=False)

    # Layout erstellen
    mainLayout = cmds.columnLayout(w = 400, h = 375)
    cmds.separator(style='none', height=25)

    # Rows fuer die einzelnen Motoren
    row1mot = cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[(1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50, height=15)
    cmds.text(label="Motor 1")
    cmds.separator(style = 'none', width = 10)
    def m1(*_):
        r.setAchse1(cmds.intField(motor1, query=True, value=True))
    motor1 = cmds.intField(cc=m1, value=int(init_pos[x - 1][y - 1][0]))
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.separator(style='none')
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row2mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 2")
    cmds.separator(style='none', width=10)
    def m2(*_):
        r.setAchse2(cmds.intField(motor2, query=True, value=True))
    motor2 = cmds.intField(minValue=-85, maxValue=50, cc=m2, value=int(init_pos[x - 1][y - 1][1]))
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(-85 - 50 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row3mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 3")
    cmds.separator(style='none', width=10)
    def m3(*_):
        r.setAchse3(cmds.intField(motor3, query=True, value=True))
    motor3 = cmds.intField(minValue=-65, maxValue=210, cc=m3, value=int(init_pos[x - 1][y - 1][2]))
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(-65 - 210 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row4mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 4")
    cmds.separator(style='none', width=10)
    def m4(*_):
        r.setAchse4(cmds.intField(motor4, query=True, value=True))
    motor4 = cmds.intField(cc=m4, value=int(init_pos[x - 1][y - 1][3]))
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.separator(style='none')
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    row5mot = cmds.rowColumnLayout(numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180)])

    cmds.separator(style='none', width=50)
    cmds.text(label="Motor 5")
    cmds.separator(style='none', width=10)
    def m5(*_):
        r.setAchse5(cmds.intField(motor5, query=True, value=True))
    motor5 = cmds.intField(minValue=-120, maxValue=120, cc=m5, value=int(init_pos[x - 1][y - 1][4]))
    cmds.separator(style='none', width=10)
    cmds.text(label="Grad")
    cmds.text(label="(-120 - 120 Grad)")
    cmds.separator(style='none', height=25)
    cmds.setParent('..')

    cmds.setParent('..')

    # Ein Layout fuer die Angabe der Sekunden zwischen den Keyframes
    table2 = cmds.rowColumnLayout( numberOfColumns=7, columnWidth=[ (1,25),(2,100),(3,10),(4,50),(5,10),(6,25),(7,180) ] )

    cmds.separator(style='none', width=50)
    cmds.text(label="Animationsabstand")
    cmds.separator(style='none', width=10)
    timedistance = cmds.intField(minValue=0, maxValue=25)
    cmds.separator(style='none', width=10)
    cmds.text(label="sek")
    cmds.text(label="(0 - 25 Sekunden)")
    cmds.separator(style='none', height=25)

    cmds.setParent('..')

    # Layout fuer den Button
    table3 = cmds.rowColumnLayout( numberOfColumns=5, columnWidth=[ (1,50),(2,150),(3,50),(4,100),(5,50) ] )

    cmds.separator(style='none', width=50, height=25)
    def setKey(*_):
        """
        Setzt den Keyframe
        :param _: metadata des Button Commands
        """
        r.setKeyframe(cmds.intField(timedistance, query=True, value=True))
    cmds.button(label='Animationspunkt setzen', command=setKey)
    cmds.separator(style='none', width=50)
    def export(*_):
        """
        Exportiert die Animation
        :param _: metadata des Button Commands
        """
        printManualAnimation()
    cmds.button(label='Drucken', command=export)
    cmds.separator(style='none', width=50)

    cmds.setParent('..')

    cmds.separator(style='none', height=25)
    # Zeigt das Fentser an

    cmds.showWindow(winID)


def SpeedUI(text):
    """
    Diese GUI wird aufgerufen sobald sich ein Motor zu schnell dreht
    :param text: der Fehlertext welcher ausgegeben wird
    """
    winID = "Speed"
    if cmds.window(winID, exists=True):
        cmds.deleteUI(winID)
    cmds.window(winID)

    masterLayout = cmds.columnLayout()

    cmds.separator(style='none', height=16)
    cmds.separator(style='in', width=300)
    cmds.separator(style='none', height=16)

    cmds.text(label=str(text), width=300)

    cmds.separator(style='none', height=16)
    cmds.separator(style='in', width=300)
    cmds.separator(style='none', height=16)

    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1, 100), (2, 100), (3, 100)])
    cmds.separator(style='none', width=100, height=25)

    def ok(*_):
        cmds.deleteUI(winID)

    cmds.button(label="OK", command=ok)
    cmds.separator(style='none', width=100, height=25)
    cmds.setParent('..')

    cmds.separator(style='none', height=25)

    cmds.showWindow(winID)

# Der Anfangs Roboterarm mitdem die parametrischen Daten erfasst werden
r = Robot("Robot")
# Oeffnen der Startpositions GUI
AnimationmodelUI()

# Testing

# w = init_pos[0][2]
# r.a1=w[0]
# r.a2=-85
# r.a3=-65
# r.a4=w[3]
# r.a5=-120
# r.updateAll()
# print("1: "+str(cmds.getAttr('achse1.rotateY')))
# print("2: "+str(cmds.getAttr('achse2.rotateZ')))
# print("3: "+str(cmds.getAttr('achse3.rotateZ')))
# print("4: "+str(cmds.getAttr('achse4.rotateX')))
# print("5: "+str(cmds.getAttr('achse5.rotateZ')))