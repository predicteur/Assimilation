# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 22:01:00 2018
@author: philippe@wlab.cc
Déclaration des constantes utilisées
"""

import os

T_MES = {'N2aixa': 4, 'N2aixc': 5, 'N2cinq': 6, 'N2plom': 7, 'N2raba': 8,
         'N2stlo': 9, 'O3aixa': 10, 'O3aixp': 11, 'O3cinq': 12, 'PCaixa': 13,
         'PCaixc': 14, 'PCcinq': 15, 'PCraba': 16, 'PCstlo': 17, 'VVaix': 18}

FILE_MES = os.path.join("data", "Biblio_2014-2015_export.csv")
FILE_PROFIL = os.path.join("export", "Resultat")
FILE_SCENARIO = os.path.join("export", "Scenario")

SEUIL_ECRETAGE = 95  # % de limitation des ecarts (pics) pour l'écrétage
