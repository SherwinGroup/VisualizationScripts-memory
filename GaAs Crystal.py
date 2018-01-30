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
import itertools as itt


app = QtWidgets.QApplication([])
mainWid = QtWidgets.QWidget()
timer = QtCore.QTimer()


wid = gl.GLViewWidget()
wid.setCameraPosition(distance=3, azimuth=22.5)
wid.setBackgroundColor("k")

# the positions of atoms in an FCC
bcc = np.array([
    [0, 0, 0],
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 0],
    [0, 1, 1],
    [1, 1, 1],

    [0, 0.5, 0.5],
    [0.5, 0, 0.5],
    [0.5, 0.5, 0],
    [0.5, 1, 0.5],
    [1, 0.5, 0.5],
    [0.5, 0.5, 1],
])

# for tiling the unit cell all over
# globalOffsets = np.array([
#     [0, 0, 0],
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1],
#     [1, 0, 1],
#     [1, 1, 0],
#     [0, 1, 1],
#     [1, 1, 1]
# ])

# No Tiling
# globalOffsets = np.array(
#     [ii for ii in itt.product(*[[0, ]]*3)]
# )
#
# # To tile into a 2x2x2
# globalOffsets = np.array(
#     [ii for ii in itt.product(*[[0, 1]]*3)]
# )
# # to tile into a 3x3x3
# globalOffsets = np.array(
#     [ii for ii in itt.product(*[[0, 1, 2]]*3)]
# )

tilingFactor = 3
globalOffsets = np.array(
    [ii for ii in itt.product(*[range(tilingFactor)]*3)]
)

mappedPoints = [] # Keep track of where you've already placed a poitn to
# prevent overlapping. There might be a smarter way to do this with tiling,
# but I'm not going for fancy here.

from OpenGL.GL import *
ptOpts = {
            GL_DEPTH_TEST: False,
            GL_BLEND: True,
            GL_ALPHA_TEST: False,
            GL_CULL_FACE: False,
            # 'glBlendFunc': (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA),
            'glBlendFunc': (GL_SRC_ALPHA, GL_ONE),
        }

for globalOffset in globalOffsets:
    Ga = []
    for coord in bcc:
        if list(coord+globalOffset )in mappedPoints: continue
        point = gl.GLScatterPlotItem(pos = coord+globalOffset, size=20, color=(.5, 1, 1, 1),
                                     glOptions="translucent")
        # point.setGLOptions(ptOpts)
        wid.addItem(point)
        mappedPoints.append(list(coord+globalOffset))


    As = []
    zboffset = np.array([0.25, 0.25, 0.25])
    for coord in bcc:
        newcoord = coord + zboffset
        if any(newcoord>1): continue
        if list(newcoord+globalOffset )in mappedPoints: continue
        point = gl.GLScatterPlotItem(pos = newcoord+globalOffset, size=20, color=(1, .5, 1, 1),
                                     glOptions="translucent")
        # point.setGLOptions(ptOpts)
        wid.addItem(point)
        mappedPoints.append(list(newcoord+globalOffset))



# Draw the edges of the cube
axes = np.array([
    np.array([0, 0, 0, 1, 0, 0]).reshape(2, 3),
    np.array([0, 0, 0, 0, 1, 0]).reshape(2, 3),
    np.array([1, 1, 0, 1, 0, 0]).reshape(2, 3),
    np.array([1, 1, 0, 0, 1, 0]).reshape(2, 3),

    np.array([0, 0, 0, 0, 0, 1]).reshape(2, 3),
    np.array([0, 1, 0, 0, 1, 1]).reshape(2, 3),
    np.array([1, 0, 0, 1, 0, 1]).reshape(2, 3),
    np.array([1, 1, 0, 1, 1, 1]).reshape(2, 3),

    np.array([0, 0, 1, 1, 0, 1]).reshape(2, 3),
    np.array([0, 0, 1, 0, 1, 1]).reshape(2, 3),
    np.array([1, 1, 1, 1, 0, 1]).reshape(2, 3),
    np.array([1, 1, 1, 0, 1, 1]).reshape(2, 3),
])

for ln in axes:
    width = 1 if ln.sum() > 1 else 4
    line = gl.GLLinePlotItem(pos = ln, color = (1, 1, 1, .5),
                             width=width)
    wid.addItem(line)

# define he vertices of the faces
oneoneone = np.array([ # [111]
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
])

oneoneonebar = np.array([ #[1 1 -1]
    [1, 0, 1],
    [0, 1, 1],
    [0, 0, 0],
])


# define he vertices of the faces, not sure if
# it matches with the tiling stuff

# mx = globalOffsets.max() +1
# oneoneone = np.array([ # (111)
#     [0, 0, mx],
#     [0, mx, 0],
#     [mx, 0, 0],
# ])
#
# oneoneonebar = np.array([ #(1 1 -1)
#     [0,  0, mx],
#     [0,  mx, 0],
#     [-mx,  0,  0],
# ])
# face = np.array([[0, 1, 2]])
#
#
# mesh = gl.GLMeshItem(vertexes = oneoneonebar, faces=face, faceColors = colors, smooth=False)
# mesh.setGLOptions('translucent')
# wid.addItem(mesh)
#
# mesh = gl.GLMeshItem(vertexes = oneoneone, faces=face, faceColors = colors, smooth=False)
# mesh.setGLOptions('translucent')
# wid.addItem(mesh)


mx = globalOffsets.max() +1
oneoneoh = np.array([ # (110)
    [0, 0, mx],
    [0, mx, 0],
    [mx, 0, mx],
    [mx, mx, 0],
])

oneohone = np.array([ #(101)
    [0,  0, mx],
    [0,  mx, mx],
    [mx,  0,  0],
    [mx,  mx,  0],
])

oneohoh = np.array([ #(100)
    [mx,  0, 0],
    [mx,  mx, 0],
    [mx,  0, mx],
    [mx,  mx, mx],
])

face = np.array([[0, 1, 2], [1, 2, 3]]) # pyGL mechanism specifying the face is between the vertices
                             # at indices 0, 1, 2

colors = np.array([[0.5, 0.5, 0.5, 0.75]]*2)

# mesh = gl.GLMeshItem(vertexes = oneoneoh, faces=face, faceColors = colors, smooth=False)
# mesh.setGLOptions('translucent')
# wid.addItem(mesh)

mesh = gl.GLMeshItem(vertexes = oneohoh, faces=face, faceColors = colors, smooth=False)
mesh.setGLOptions('translucent')
wid.addItem(mesh)

x = pd.ExcelFile(os.path.join(directory, filename))
wid.show()
app.exec_()




# g1 = gl.GLGridItem()
# g1.setSpacing(0.1, 0.1, 0.1)
# g1.setSize(2,2,2)
#
# piYvsTime = gl.GLLinePlotItem(color=(1,0,0,1), width=2)
# piYProj = gl.GLLinePlotItem(color=(1,0,0,1), width=2)
#
# piXvsTime = gl.GLLinePlotItem(color=(0,1,0,1), width=2)
# piXProj = gl.GLLinePlotItem(color=(0,1,0,1), width=2)
#
# piElliptical = gl.GLLinePlotItem(color=(.5,.5,1,1), width=2)
# piEllipticalStatic = gl.GLLinePlotItem()

# app.exec_()
