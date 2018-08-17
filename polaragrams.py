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

from hsganalysis.jones import JonesVector as JV
import interactivePG as ipg

cos = lambda x: np.cos(x*np.pi/180)
sin = lambda x: np.sin(x*np.pi/180)
#
# def wavePlate(t, d):
#     d = d* 2 * np.pi
#     t = 2*t
#     return np.array([
#         [1, 0, 0, 0],
#         [0, cos(t)**2+cos(d)*sin(t)**2, cos(t)*sin((t)*(1-cos(d)), sin(t)*sin(d))],
#         [0, cos(t)*sin((t)*(1-cos(d)), sin(t)**2+cos(d)*cos(t)**2, -cos(t)*sin(d))],
#         [0, -sin(t)*sin(d), cos(t)*sin(d), cos(d)]
#     ])
#
#
#
# class StokeVector(object):
#     def __init__(alpha=0, gamma=0, dop=1):
#         S0 = 1
#         S1 = dop * np.cos(2 * alpha * np.pi / 180) * np.cos(2 * gamma * np.pi / 180)
#         S2 = dop * np.sin(2 * alpha * np.pi / 180) * np.cos(2 * gamma * np.pi / 180)
#         S3 = dop * np.sin(2 * gamma * np.pi / 180)
#
#         self.vec = np.array([S0, S1, S2, S3])
#
#     def apply_retarder(t, d):
#         np.


def analyzerCurve(alpha=0, gamma=0, dop=1, eta=0.25):
    S0 = 1
    S1 = dop * np.cos(2 * alpha * np.pi / 180) * np.cos(2 * gamma * np.pi / 180)
    S2 = dop * np.sin(2 * alpha * np.pi / 180) * np.cos(2 * gamma * np.pi / 180)
    S3 = dop * np.sin(2 * gamma * np.pi / 180)
    x = np.linspace(0, 360, 500)
    eta *= 2*np.pi
    int= S0+S1/2*(1+np.cos(eta)) \
           - S3*np.sin(eta)*sin(2*x) \
           + S1/2*(1-np.cos(eta))*cos(4*x) \
           + S2/2*(1-np.cos(eta))*sin(4*x)
    int /= int.max()
    return [x, int]

def storeCurve():
    curve = window.recalculate()


    window.plot(*curve, name=",".join([":".join([str(ii) for ii in jj])
                                        for jj in window.getCurrentValues()]))



app = QtWidgets.QApplication([])


window = ipg.ManipulateWindow()
window.plot(*analyzerCurve())
window.setManipulators([
    ("&alpha;", [-90, 90, 0, 1]),
    ("&gamma;", [-45, 45, 0, 1]),
    ("DOP", [0, 1, 1, 0.01]),
    ("&eta;", [0.2, 0.3, 0.25, 0.01]),
])
window.setCallable(analyzerCurve)

window.plotItem.setLabel("bottom", "QWP Angle (°)")
window.plotItem.setLabel("left", "Normalized Intensity")
window.plotItem.setYRange(0, 1, padding=0)
window.plotItem.setXRange(-5, 365, padding=0)
window.plotItem.axes["bottom"]["item"].setTickSpacing(45, 15)
window.plotItem.axes["top"]["item"].setTickSpacing(45, 15)

window.plotItem.setLabel("bottom", "Sideband Order")

b = QtWidgets.QPushButton("Store Curve")
b.clicked.connect(storeCurve)
window.centralWidget().layout().insertWidget(1, b)
window.addLegend()

window.show()

from pyqtgraph.console import ConsoleWidget as CW
c = CW(namespace={"w":window, "wid":QtWidgets, "ipg":ipg})
c.show()



app.exec_()
