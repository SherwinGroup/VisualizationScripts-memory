# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 15:41:33 2014

@author: dvalovcin
"""

from __future__ import division
import numpy as np
from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl



app = QtWidgets.QApplication([])
mainWid = QtWidgets.QWidget()
timer = QtCore.QTimer()
def togglePause(val):
    if val:
        timer.stop()
    else:
        timer.start()


def update():
    tim = sbTime.value()
    if timer.isActive():
        tim = (sbTime.value()+1)%360
        sbTime.blockSignals(True)
        sbTime.setValue(tim)
        sbTime.blockSignals(False)
    tim *= np.pi/180.

    t = np.linspace(0, 2*np.pi, 100)
    amp1 = np.cos(sbPhi.value()*np.pi/180.)*np.sin(t+tim)
    amp2 = np.sin(sbPhi.value()*np.pi/180.)*np.sin(t+sbDelta.value()*np.pi/180. +tim)
    inplane = np.zeros_like(t)


    piYvsTime.setData(pos=np.column_stack((inplane, amp1, t)))
    piYProj.setData(pos=np.column_stack((inplane, amp1, inplane)))

    piXvsTime.setData(pos=np.column_stack((amp2, inplane, t)))
    piXProj.setData(pos=np.column_stack((amp2, inplane, inplane)))


    piElliptical.setData(pos=np.column_stack((amp2, amp1, t)))
    piEllipticalStatic.setData(pos=np.column_stack((amp2, amp1, inplane)))

def updateEllipseValues():
    phi = sbPhi.value()*np.pi/180.
    mag = [np.cos(phi), np.sin(phi)]
    Ex,Ey = mag
    ang = [0, sbDelta.value()*np.pi/180.]
    inpPol = np.arctan2(2*mag[0]*mag[1]*np.cos(ang[1]-ang[0]), (mag[0]**2-mag[1]**2))/2*180/3.14159
    ratio = np.arcsin(2*mag[0]*mag[1]*np.sin(ang[1]-ang[0])/(mag[0]**2+mag[1]**2))/2*180/3.14159

    sbEllAngle.blockSignals(True)
    sbEllAxes.blockSignals(True)
    sbPhi.blockSignals(True)

    sbEllAngle.setValue(np.round(inpPol,1))
    sbEllAxes.setValue(np.round(ratio,1))
    sbEllAngle.setValue(inpPol,1)
    sbEllAxes.setValue(ratio,1)


    sbEllAngle.blockSignals(False)
    sbEllAxes.blockSignals(False)
    sbPhi.blockSignals(False)

    update()

def updateEFieldValues():
    gamma = sbEllAxes.value()*np.pi/180.
    alpha = sbEllAngle.value()*np.pi/180.

    vec = np.array([np.cos(gamma), 1j*np.sin(gamma)])[:,None]
    rot = np.array([[np.cos(alpha), -np.sin(alpha)],
                    [np.sin(alpha), np.cos(alpha)]])
    vec = np.dot(rot,vec)


    ratio = np.abs(vec[1])/np.abs(vec[0])
    phi = np.arctan2(np.abs(vec[1]), np.abs(vec[0]))
    delta = np.angle(vec[1], deg=True) - np.angle(vec[0], deg=True)

    sbPhi.blockSignals(True)
    sbDelta.blockSignals(True)
    print("p/d", phi, delta[0])
    sbPhi.setValue(phi[0]*180./np.pi)
    sbDelta.setValue(delta[0])

    sbPhi.blockSignals(False)
    sbDelta.blockSignals(False)



    update()

wid = gl.GLViewWidget()
wid.setCameraPosition(distance=3, azimuth=22.5)
g1 = gl.GLGridItem()
g1.setSpacing(0.1, 0.1, 0.1)
g1.setSize(2,2,2)

piYvsTime = gl.GLLinePlotItem(color=(1,0,0,1), width=2)
piYProj = gl.GLLinePlotItem(color=(1,0,0,1), width=2)

piXvsTime = gl.GLLinePlotItem(color=(0,1,0,1), width=2)
piXProj = gl.GLLinePlotItem(color=(0,1,0,1), width=2)

piElliptical = gl.GLLinePlotItem(color=(.5,.5,1,1), width=2)
piEllipticalStatic = gl.GLLinePlotItem()
wid.addItem(piYvsTime)
wid.addItem(piYProj)
wid.addItem(piXvsTime)
wid.addItem(piXProj)
wid.addItem(piElliptical)
wid.addItem(piEllipticalStatic)
wid.addItem(g1)




optionsLayout = QtWidgets.QFormLayout()
overallLayout = QtWidgets.QHBoxLayout()

sbPhi = pg.SpinBox(value=45, bounds=(-90, 90), step=1, decimals=3)
sbPhi.sigValueChanging.connect(updateEllipseValues)
sbDelta = pg.SpinBox(value=0, bounds=(-180,180), step=1, decimals=3)
sbDelta.sigValueChanging.connect(updateEllipseValues)


sbEllAxes = pg.SpinBox(value=0, bounds=(-180, 180), step=1, decimals=3)
sbEllAxes.sigValueChanging.connect(updateEFieldValues)
sbEllAngle = pg.SpinBox(value=45, bounds=(-180, 180), step=1, decimals=3)
sbEllAngle.sigValueChanging.connect(updateEFieldValues)
sbTime = pg.SpinBox(value=0, bounds=(0, 360), step=1)
sbTime.sigValueChanging.connect(update)


sbSpeed = pg.SpinBox(value=30, bounds=(1, 250), step=1)
sbSpeed.sigValueChanging.connect(lambda x: timer.setInterval(x.value()))

optionsLayout.addRow("φ (°)", sbPhi)
optionsLayout.addRow("δ (°)", sbDelta)
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow("γ (°)", sbEllAxes)
optionsLayout.addRow("α (°)", sbEllAngle)
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())

optionsLayout.addRow("Time", sbTime)
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())
optionsLayout.addRow(QtWidgets.QVBoxLayout())



optionsLayout.addRow("Speed", sbSpeed)
bPause = QtWidgets.QPushButton("Pause")
bPause.setCheckable(True)
bPause.clicked.connect(togglePause)
optionsLayout.addRow(bPause)

overallLayout.addLayout(optionsLayout)
overallLayout.addWidget(wid)
overallLayout.setStretch(0, 2)
overallLayout.setStretch(1, 10)
mainWid.setLayout(overallLayout)
mainWid.setGeometry(150,150,800, 600)
mainWid.show()







update()
timer.timeout.connect(update)
timer.setInterval(30)
timer.start()

app.exec_()
