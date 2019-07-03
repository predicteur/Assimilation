# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 23:27:17 2018
@author: philippe@wlab.cc
"""
from math import sqrt, pi, exp, log


class Vecteur():
    """
    utilisation de vecteur
    """

    # initialisation
    def __init__(self, p1, p2):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

    # surcharges
    def __add__(a, b):
        return Vecteur(a.x + b.x, a.y + b.y)

    # méthodes
    def norme(self):
        return sqrt(self.x**2 + self.y**2)

    def produitScalaire(self, b):
        return self.x * b.x + self.y * b.y

    def cosinus(self, b):
        if b.norme() < 0.00001 or self.norme() < 0.00001:
            cos = 1.0
        else:
            cos = self.produitScalaire(b)/self.norme()/b.norme()
        return cos


class Point:
    """
    utilisation de point
    """
    def __init__(self, x=0.0, y=0.0):
        self.x, self.y = x, y

    def __eq__(self, pointB):
        return self.x == pointB.x and self.y == pointB.y

    def __str__(self):
        """affichage point"""
        return "x;{};y;{}".format(self.x, self.y)

    # méthodes
    def translation(self, point, vect):
        return Point(point.x+vect.x, point.y+vect.y)

    def dist(self, p2):
        return sqrt((self.x - p2.x)**2 + (self.y - p2.y)**2)


class Segment:
    """
    utilisation de segments
    équation : ax+by+c = 0
    a = y2-y1, b = x1-x2, c = y1(x2-x1) - x1(y2-y1)
    distance A : |a xa + b ya + c|/sqrt(a**2+b**2)
    """
    def __init__(self, p1, p2):
        self.p1, self.p2 = p1, p2
        self.a = self.p2.y - self.p1.y
        self.b = self.p1.x - self.p2.x
        self.c = self.p1.y * (self.p2.x - self.p1.x) -\
            self.p1.x * (self.p2.y - self.p1.y)
        self.long = sqrt((self.p1.x - self.p2.x)**2 +
                         (self.p1.y - self.p2.y)**2)

    # méthodes
    def point(self, dist=0.0):
        return Point(self.p1.x*(1.0-dist)+self.p2.x*dist,
                     self.p1.y*(1.0-dist)+self.p2.y*dist)

    def longueur(self):
        return self.long

    def dist(self, point):
        cos1 = Vecteur(self.p1, self.p2).cosinus(Vecteur(self.p1, point))
        cos2 = Vecteur(self.p2, self.p1).cosinus(Vecteur(self.p2, point))
        if cos1 > 0.0 and cos2 > 0.0:
            distance = abs(self.a*point.x+self.b*point.y+self.c) / \
                       sqrt(self.a**2+self.b**2)
        else:
            distance = min(point.dist(self.p1), point.dist(self.p2))
        return distance


class Normale:
    """
    utilisation de loi normale (aire : aire, sigma : écart-type)
    vmax = aire/sig/racine(2*pi)
    val = vmax*exp(-0,5(dist/sig)**2)
    dist = sig*racine(2*log(vmax/val))
    """
    def __init__(self, aire, sigma):
        self.aire, self.sigma = aire, sigma
        self.vmax = self.aire/self.sigma/sqrt(2.0*pi)

    # méthodes
    def dist(self, val):
        return self.sigma * sqrt(2.0 * log(self.vmax / val))

    def val(self, dist=0.0):
        return self.vmax * exp(-0.5 * (dist / self.sigma)**2)


class Pente:
    """
    utilisation d'une pente (aire : aire, sigma : distance max)
    vmax = aire/sigma
    val = vmax(1-dist/sigma)
    dist = sigma(1-val/vmax)
    """
    def __init__(self, aire, sigma):
        self.aire, self.sigma = aire, sigma
        self.vmax = self.aire / self.sigma

    # méthodes
    def dist(self, val):
        return self.sigma * (1.0 * val / self.vmax)

    def val(self, dist=0.0):
        return max(0.0, self.vmax * (1.0 - dist / self.sigma))
