# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 22:55:07 2018
@author: philippe@wlab.cc
"""
from numpy import zeros, vectorize, amin, amax, dot, identity, diag,\
    linalg, array
from vecteur import Point
from math import exp, sqrt


class Profil:
    """
    Methodes liees aux profils.
    """
    def __init__(self, p1, p2, pas, sources, mesures):
        """
        Initialisation du profil
        """
        self.pas = pas
        self.taillex = int(abs(p1.x - p2.x)/self.pas) + 1
        self.tailley = int(abs(p1.y - p2.y)/self.pas) + 1
        self.prof = zeros((self.taillex, self.tailley))
        self.profXmin = min(p1.x, p2.x)
        self.profXmax = max(p1.x, p2.x)
        self.profYmin = min(p1.y, p2.y)
        self.profYmax = max(p1.y, p2.y)
        self.sources = sources
        self.mesures = mesures

    def profil(self):
        """
            restitution profil
        """
        return self.prof

    def valMin(self):
        """
            valeur mini du profil
        """
        return amin(self.prof)

    def valMax(self):
        """
            valeur maxi du profil
        """
        return amax(self.prof)

    def valMoy(self):
        """
            valeur moyenne du profil
        """
        return self.prof.mean()

    def point(self, a):
        """
            point à partir des coordonnées
        """
        return Point(self.profXmin+self.pas*a[0], self.profYmin+self.pas*a[1])

    def coord(self, p):
        """
            coordonnées d'un point
        """
        c1 = zeros((2), dtype=int)
        c1[0] = round((p.x - self.profXmin)/self.pas)
        c1[1] = round((p.y - self.profYmin)/self.pas)
        return c1

    def addSourceGrille(self):
        """
            contribution des sources par grille
        """
        for src in self.sources:
            self.prof += src.grille(self)
        return self.prof

    def addSources(self):
        """
            contribution des sources
        """
        coor = zeros((2), dtype=int)
        for i in range(self.taillex):
            for j in range(self.tailley):
                coor[:] = i, j
                self.prof[i, j] += self.valSources(self.point(coor))

    def valSources(self, point):
        """
            valeur du cumul des sources en un point
        """
        valeur = 0.0
        for src in self.sources:
            valeur += src.valeur(point)
        return valeur

    def valeur(self, point, exp=2):
        """
            valeur en un point quelconque
        """
        cx = int(abs(point.x - self.profXmin)//self.pas)
        cy = int(abs(point.y - self.profYmin)//self.pas)
        dx = (point.x - self.profXmin - cx * self.pas) / self.pas
        dy = (point.y - self.profYmin - cy * self.pas) / self.pas
        d1 = sqrt(dx**2 + dy**2)
        d2 = sqrt((1.0-dx)**2 + dy**2)
        d3 = sqrt(dx**2 + (1.0-dy)**2)
        d4 = sqrt((1.0-dx)**2 + (1.0-dy)**2)
        return (self.prof[cx, cy]*(d2*d3*d4)**exp +
                self.prof[cx+1, cy]*(d1*d3*d4)**exp +
                self.prof[cx, cy+1]*(d1*d2*d4)**exp +
                self.prof[cx+1, cy+1]*(d1*d2*d3)**exp) /\
            ((d2*d3*d4)**exp + (d1*d3*d4)**exp + (d1*d2*d4)**exp +
                (d1*d2*d3)**exp)

    def seuilBas(self, seuil):
        """
            seuil bas sur profil
        """
        def f(x): return seuil if x < seuil else x
        vf = vectorize(f)
        self.prof = vf(self.prof)

    def seuilHaut(self, seuil):
        """
            seuil haut sur profil
        """
        def f(x): return seuil if x > seuil else x
        vf = vectorize(f)
        self.prof = vf(self.prof)

    def ajout(self, prof):
        """
             ajout d'une valeur de profil sur profil
        """
        self.prof += prof
        return self.prof

    def recalage(self, modele, sigb, sigmod, dist):
        """
            recalage du profil par le modèle
        """

        xb = self.prof.reshape(self.taillex * self.tailley)
        y = array(modele)
        h = zeros((y.size, xb.size))

        h[0, 0:3] = [1, 1, 1]
        h[0, self.taillex:self.taillex+3] = [1, 1, 1]
        h[0, 2*self.taillex:2*self.taillex+3] = [1, 1, 1]

        h[1, 3:6] = [1, 1, 1]
        h[1, self.taillex+3:self.taillex+6] = [1, 1, 1]
        h[1, 2*self.taillex+3:2*self.taillex+6] = [1, 1, 1]

        h[2, 3*self.taillex:3*self.taillex+3] = [1, 1, 1]
        h[2, 4*self.taillex:4*self.taillex+3] = [1, 1, 1]
        h[2, 5*self.taillex:5*self.taillex+3] = [1, 1, 1]

        h[3, 3*self.taillex+3:3*self.taillex+6] = [1, 1, 1]
        h[3, 4*self.taillex+3:4*self.taillex+6] = [1, 1, 1]
        h[3, 5*self.taillex+3:5*self.taillex+6] = [1, 1, 1]
        # print('h ', h)
        h /= 9.0
        r = identity(y.size) * sigmod**2
        b = zeros((xb.size, xb.size))
        for xi in range(xb.size):
            for xj in range(xb.size):
                xii = (xi) // self.tailley
                xij = xi - xii * self.tailley
                xji = (xj) // self.tailley
                xjj = xj - xji * self.tailley
                dij2 = (xii - xji)**2 + (xij - xjj)**2
                # b[xi, xj] = dij2
                b[xi, xj] = sigb**2 * exp(-0.5 * dij2 / dist**2)
        # for i in range(xb.size):
        #    for j in range(xb.size):
        #        b[i, j] = sigb**2 * exp(-0.5 * abs(i-j) / dist)
        k = dot(dot(b, h.T), linalg.inv(dot(dot(h, b), h.T) + r))
        xa = xb + dot(k, y - dot(h, xb))
        self.prof = xa.reshape(self.taillex, self.tailley)

    def lissage(self, sigma):
        """
            lissage sur les points (sigma entre 0.3 et 0.7)
        """
        v1 = exp(-0.5/sigma**2)
        v2 = exp(-1/sigma**2)
        v0 = 1.0 / (1 + 4 * v1 + 4 * v2)
        v1 *= v0
        v2 *= v0
        coor = zeros((2), dtype=int)
        profl = self.prof + 0.
        for i in range(1, self.taillex-1):
            for j in range(1, self.tailley-1):
                coor[:] = i, j
                profl[i, j] = self.prof[i, j] * v0 +\
                    (self.prof[i-1, j] + self.prof[i+1, j]) * v1 +\
                    (self.prof[i, j-1] + self.prof[i, j+1]) * v1 +\
                    (self.prof[i-1, j-1] + self.prof[i+1, j+1]) * v2 +\
                    (self.prof[i-1, j+1] + self.prof[i+1, j-1]) * v2
        self.prof = profl + 0.

    def ajustement(self, amjh, filtrage, ajust, sigb, dist):
        """
            ajustement du profil aux mesures
        """
        coef = zeros((self.taillex, self.tailley))
        y = zeros((len(self.mesures)))
        sig2 = zeros((len(self.mesures)))
        i = 0
        for mes in self.mesures:
            if filtrage == 'ecretage':
                y[i] = mes.mesEcre(amjh)
            elif filtrage == 'filtrage':
                y[i] = mes.mesEcreF(amjh)
            else:
                y[i] = mes.mesBrut(amjh)
            sig2[i] = mes.sig**2
            coef[self.coord(mes.pos)[0], self.coord(mes.pos)[1]] = y[i] /\
                self.prof[self.coord(mes.pos)[0], self.coord(mes.pos)[1]]
            i += 1
        if ajust == 'BLUE':
            xb = self.prof.reshape(self.taillex * self.tailley)
            h = zeros((y.size, xb.size))
            for i in range(y.size):
                j = self.coord(self.mesures[i].pos)[0]*self.tailley + \
                    self.coord(self.mesures[i].pos)[1]
                h[i, j] = 1
            r = diag(sig2)
            b = zeros((xb.size, xb.size))
            for xi in range(xb.size):
                for xj in range(xb.size):
                    xii = (xi) // self.tailley
                    xij = xi - xii * self.tailley
                    xji = (xj) // self.tailley
                    xjj = xj - xji * self.tailley
                    dij2 = (xii - xji)**2 + (xij - xjj)**2
                    # b[xi, xj] = dij2
                    b[xi, xj] = sigb**2 * exp(-0.5 * dij2 / dist**2)
            k = dot(dot(b, h.T), linalg.inv(dot(dot(h, b), h.T) + r))
            xa = xb + dot(k, y - dot(h, xb))
            self.prof = xa.reshape(self.taillex, self.tailley)
            '''# print('b0 ', b[1, :].reshape(6, 6))
                # print('x ', self.coord(self.mesures[i].pos)[0])
                # print('y ', self.coord(self.mesures[i].pos)[1])
            print('k ', k)
            # print('tx, ty ', self.taillex, self.tailley)
            print('r ', r)
            print('h*xb ', dot(h, xb))
            print('h*b*ht ', dot(dot(h, b), h.T))
            print('xb ', xb)
            print('y ', y)
            print('h ', h)
            print('xa ', xa)'''
        elif ajust != 'aucun':
            for i in range(self.taillex):
                for j in range(self.tailley):
                    trouve = False
                    coefij = 0.0
                    distij = 0.0
                    for mes in self.mesures:
                        if mes.pos == self.point([i, j]):
                            trouve = True
                        if not(trouve):
                            coefij += coef[self.coord(mes.pos)[0],
                                           self.coord(mes.pos)[1]] / \
                                      mes.pos.dist(self.point([i, j]))
                            distij += 1 / mes.pos.dist(self.point([i, j]))
                    if not(trouve):
                        coef[i, j] = coefij / distij
            self.prof *= coef

    def export(self, nomFichier):
        """
            export d'un profil vers excel
        """
        fichier = nomFichier + '.csv'

        # parametres principaux en premiere ligne
        with open(fichier, 'w') as fic:
            # parametres
            ligne = '  ' + ";"
            ligne += "Pas " + str(self.pas) + ";"
            ligne += "Taillex " + str(self.taillex) + ";"
            ligne += "Tailley " + str(self.tailley) + ";"
            ligne += "Xmin  " + str(self.profXmin) + ";"
            ligne += "Xmax  " + str(self.profXmax) + ";"
            ligne += "Ymin  " + str(self.profYmin) + ";"
            ligne += "Ymax  " + str(self.profYmax) + ";"
            ligne += "\n"
            fic.write(ligne)
            fic.write('  ' + '\n')

            # entete des colonnes
            ligne = '  ' + ";" + ";"
            for j in range((self.tailley)):
                ligne += str(j)[0:3] + ';'
            ligne += '\n'
            fic.write(ligne)

            # resultats par ligne
            for i in range((self.taillex)):
                ligne = '  ' + ";" + str(i)[0:3] + ";"
                for j in range((self.tailley)):
                    ligne += str(self.prof[i, j]
                                 ).replace(".", ",") + ';'
                ligne += '\n'
                fic.write(ligne)
        return
