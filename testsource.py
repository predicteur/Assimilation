# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 22:39:20 2018
@author: philippe@wlab.cc
"""

from scenario import Scenario
from vecteur import Point
from numpy import array, set_printoptions
from sourcemesure import mess, srcs


def testSource():

    set_printoptions(precision=2, linewidth=100, suppress=True)
    scenar1 = Scenario(point1=Point(1.0, 1.0),
                       point2=Point(26.0, 26.0),
                       pas=5,
                       sources=srcs,
                       mesures=mess)

    scenar1.initSequence(array([2014, 1, 1, 1]),
                         array([2014, 1, 1, 2]))
    print('duree', scenar1.duree)

    scenar1.execution(ajust='BLUE',
                      filtrage='ecretage',
                      lissage=0,
                      seuilB=5,
                      dist=3,
                      sigb=1,
                      sigmod=0.1,
                      modele=[40./9., 20./9., 0, 0])

testSource()
