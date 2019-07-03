# -*- coding: utf-8 -*-
"""
Created on Sat Jan  6 23:27:00 2018
@author: philippe@wlab.cc
"""
from constante import T_MES, FILE_MES, SEUIL_ECRETAGE
from numpy import loadtxt, array_equal, percentile, roll, zeros
from datetime import datetime, timedelta


def lireMesure():
    """
    chargement et initialisation des données de mesures
    Structure du fichier csv FILE_MESURE :
        annee, mois, jour, heure : colonnes 0 à 3
        mesure : colonne n° serie_dans T_MES
    """
    return loadtxt(FILE_MES, delimiter=';', skiprows=1)


def amjhi(amjh, i):
    date = datetime(int(amjh[0]), int(amjh[1]),
                    int(amjh[2]), int(amjh[3])) + i*timedelta(0, 3600)
    amjh2 = zeros((4))
    amjh2[0] = date.year
    amjh2[1] = date.month
    amjh2[2] = date.day
    amjh2[3] = date.hour
    return amjh2


class Mesure():
    """
    utilisation de mesures
    """
    def __init__(self, pol, nom, pos, sig=0.1):
        """
        Initialisation d'une mesure
        """
        self.nom = nom
        self.pos = pos
        self.sig = sig
        self.pol = pol
        self.mes = lireMesure()
        self.seuil = percentile(self.mes[:, T_MES[self.pol+self.nom]] -
                                roll(self.mes[:, T_MES[self.pol+self.nom]],
                                     1), SEUIL_ECRETAGE)
        self.lignes = self.mes[:, 0].size
        self.noPol = T_MES[self.pol+self.nom]

    def __str__(self):
        """affichage mesure"""
        return "nom;{};polluant;{};position;{};sigma;{};".format(
                self.nom, self.pol, self.pos, self.sig)

    def mesBrut(self, amjh):
        """
        Acquisition d'une valeur horaire
        """
        valh = -1.0
        for i in range(self.lignes):
            if array_equal(amjh[:], self.mes[i, 0:4]):
                valh = self.mes[i, self.noPol]
        return valh

    def mesEcre(self, amjh):
        """
        Acquisition d'une valeur écrétée
        """
        vale = -1.0
        for i in range(self.lignes):
            if array_equal(amjh[:], self.mes[i, 0:4]):
                vale = self.mes[i, self.noPol]
                if vale - self.mes[i-1, self.noPol] > self.seuil:
                    vale = self.mes[i-1, self.noPol] + self.seuil
        return vale

    def mesEcreF(self, amjh):
        """
        Acquisition d'une valeur écrétée filtrée
        """
        valf = -1.0
        for i in range(self.lignes):
            if array_equal(amjh[:], self.mes[i, 0:4]):
                if i < 5 or i == self.lignes - 1:
                    valf = self.mesEcre(amjh)
                else:
                    valf = self.mesEcre(amjhi(amjh, -5))
                    for j in range(4, -1, -1):
                        valf = 0.5 * valf +\
                            0.25 * self.mesEcre(amjhi(amjh, -j)) +\
                            0.25 * self.mesEcre(amjhi(amjh, -j+1))
        return valf
'''
arr = np.arange(12).reshape((3, 4))
condition = arr[:,0:3] == [ 4,  5,  6]
np.extract(condition, arr)
'''
