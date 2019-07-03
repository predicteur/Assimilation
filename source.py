# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 22:18:36 2018
@author: philippe@wlab.cc
"""
from vecteur import Normale, Segment, Point, Pente
from numpy import zeros


class Source:
    """
    Methodes liees aux sources.
    """

    def __init__(self, types, loi, valeur, sig, ps1, ps2=Point()):
        self.centre = ps1
        self.centre2 = ps2
        self.surface = valeur
        self.sig = sig
        self.loi = loi
        self.types = types

    def __str__(self):
        """affichage sources"""
        return "type;{};loi;{};surface;{};sigma;{};point1;{};point2;{};".\
            format(self.types, self.loi, self.surface, self.sig, self.centre,
                   self.centre2)

    def valeur(self, point):
        """
            calcul contribution sur un point
        """
        if self.types == 'ponctuelle':
            if self.loi == 'n':
                val = Normale(self.surface, self.sig)\
                    .val(self.centre.dist(point))
            else:
                val = Pente(self.surface, self.sig)\
                    .val(self.centre.dist(point))
        else:
            if self.loi == 'n':
                val = Normale(self.surface, self.sig)\
                    .val(Segment(self.centre, self.centre2).dist(point))
            else:
                val = Pente(self.surface, self.sig)\
                    .val(Segment(self.centre, self.centre2).dist(point))
        return val

    def grille(self, prof):
        """
            calcul contribution de la source sur la grille
        """
        gr = zeros((prof.taillex, prof.tailley))
        coor = zeros((2), dtype=int)
        for i in range(prof.taillex):
            for j in range(prof.tailley):
                coor[:] = i, j
                gr[i, j] = self.valeur(prof.point(coor))
        return gr
