# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 23:56:19 2018

@author: philippe@wlab.cc
"""
from numpy import zeros, array
from vecteur import Point
from constante import FILE_PROFIL, FILE_SCENARIO
from datetime import datetime, timedelta
from profil import Profil


def export(nomFichier, sigb, dist, filtrage,
           ajust, seuilB, seuilH, lissage, sigma, debut, fin, duree,
           mesures, sources):
    """
        export d'un scenario vers excel
    """
    fichier = nomFichier + '.csv'

    with open(fichier, 'w') as fic:
        ligne = "parametres :" + '\n'
        ligne += ";sigb;" + str(sigb).replace(".", ",") + '\n'
        ligne += ";dist;" + str(dist).replace(".", ",") + '\n'
        ligne += ";filtrage;" + filtrage + '\n'
        ligne += ";ajust;" + ajust + '\n'
        ligne += ";seuilB;" + str(seuilB).replace(".", ",") + '\n'
        ligne += ";seuilH;" + str(seuilH).replace(".", ",") + '\n'
        ligne += ";lissage;" + str(lissage).replace(".", ",") + '\n'
        ligne += ";sigma;" + str(sigma).replace(".", ",") + '\n'
        ligne += ";debut(amjh);" + str(debut[0]) + ';' + str(debut[1]) + ';' +\
            str(debut[2]) + ';' + str(debut[3]) + '\n'
        ligne += ";fin(amjh);" + str(fin[0]) + ';' + str(fin[1]) + ';' +\
            str(fin[2]) + ';' + str(fin[3]) + '\n'
        ligne += ";duree;" + str(duree).replace(".", ",") + '\n' + "\n"
        fic.write(ligne)
        ligne = "mesures :" + '\n'
        for mes in mesures:
            ligne += ";" + str(mes).replace(".", ",") + '\n'
        fic.write(ligne + '\n')
        ligne = "sources :" + '\n'
        for src in sources:
            ligne += ";" + str(src).replace(".", ",") + '\n'
        fic.write(ligne + '\n')


class Scenario:
    """
    Methodes liees aux scénarios.
    """
    def __init__(self, point1=Point(0.0, 0.0), point2=Point(10.0, 10.0),
                 pas=1.0, sources=[], mesures=[],
                 debut=array([2014, 1, 1, 1]), fin=array([2014, 1, 2, 1]),
                 sortie=FILE_SCENARIO):
        """
        Initialisation du scenario
        """
        self.pas = pas
        self.point1 = point1
        self.point2 = point2
        self.sources = sources
        self.mesures = mesures
        self.debut = debut
        self.fin = fin
        self.sortie = sortie
        self.profil = Profil(self.point1, self.point2, self.pas, self.sources,
                             self.mesures)
        self.initSequence(self.debut, self.fin)

    def initSequence(self, debut, fin):
        """
            initialisation temporelle du scénario
        """
        self.debut = debut
        self.fin = fin
        diff = datetime(int(self.fin[0]), int(self.fin[1]),
                        int(self.fin[2]), int(self.fin[3])) -\
            datetime(int(self.debut[0]), int(self.debut[1]),
                     int(self.debut[2]), int(self.debut[3]))
        self.duree = int(diff.days*24.0 + diff.seconds/3600.0)

    def execution(self, sigb=1., dist=10., filtrage='ecretage',
                  ajust='barycentre', seuilB=0.001, seuilH=1000.0, lissage=1,
                  sigma=0.5, modele=[0, 0, 0, 0], sigmod=1):
        """
            déroulement du scénario
        """
        datet = datetime(int(self.debut[0]), int(self.debut[1]),
                         int(self.debut[2]), int(self.debut[3]))
        for i in range(self.duree):
            amjh = [datet.year, datet.month, datet.day, datet.hour]
            self.profil.prof = zeros((self.profil.taillex,
                                      self.profil.tailley))
            self.profil.addSources()
            print('addsources', '\n', self.profil.prof)
            self.profil.recalage(modele, sigb, sigmod, dist)
            print('recalage ')
            self.profil.seuilBas(seuilB)
            print('seuilbas ', seuilB)
            self.profil.seuilHaut(seuilH)
            print('seuilhaut ', seuilH)
            self.profil.ajustement(amjh, filtrage, ajust, sigb, dist)
            print('ajustement mesure ',  amjh)
            for i in range(lissage):
                self.profil.lissage(sigma)
                print('lissage ', sigma)
            print('profil', '\n', self.profil.prof)
            fichier = FILE_PROFIL + str(i)
            self.profil.export(fichier)
            datet += timedelta(0, 3600)
        export(self.sortie, sigb, dist, filtrage,
               ajust, seuilB, seuilH, lissage, sigma,
               self.debut, self.fin, self.duree, self.mesures, self.sources)
