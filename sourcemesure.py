# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 23:20:16 2018
@author: philippe@wlab.cc
"""
from vecteur import Point
from mesure import Mesure
from source import Source

pm0 = Point(21.0, 21.0)
pm1 = Point(6.0, 6.0)  # était 6,1

mess = [Mesure('PC', 'aixa', pm0, 0.1),
        Mesure('PC', 'aixc', pm1, 0.1)]

ps0 = Point(6.0, 6.0)
ps1 = Point(11.0, 11.0)
ps2 = Point(11.0, 16.0)

srcs = [Source('ponctuelle', 'p', 100.0, 5.0, ps0),
        Source('segment', 'p', 100.0, 5.0, ps1, ps2)]
