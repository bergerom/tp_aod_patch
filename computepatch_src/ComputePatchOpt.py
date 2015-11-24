#!/usr/bin/env python3

# Classe qui calcule le patch de cout minimal
# Utilisation : python ComputePatchOpt fichier1 fichier2
import os
from PatchAtom import *
from Patch import *
import sys

class Infinity:
    def __lt__(self, other):
        return False
    def __le__(self, other):
        return False
    def __gt__(self, other):
        return True
    def __ge__(self, other):
        return True
    def __add__(self, other):
        return self
    def __radd__(self, other):
        return self

INFINITY = Infinity()

class TabPatch:
    def __init__(self, file_before_patch, file_after_patch):

            self.file_before_patch = file_before_patch
            self.file_after_patch = file_after_patch
            self.nb_line_n1 = len(self.file_before_patch)
            self.nb_line_n2 = len(self.file_after_patch)

            # Conditions limites

            # Initialisation de memo_min, dont chaque case j contient
            # le patch de cout minimum sur i
            self.memo_min = []
            p = Patch()
            p.cost = INFINITY
            for line in range(0, self.nb_line_n2 + 1):
                self.memo_min.append(p)
            # memo_cur contient les Patchs de la ligne i courante
            self.memo_cur = []
            # memo_prec contient les Patchs de la ligne précédente (i-1)
            self.memo_prec = []
            i = 0
            p = Patch()
            self.memo_prec.append(p)
            for line in self.file_after_patch:
                p = p.copy_and_add(AdditionAtom(i, line))
                self.memo_prec.append(p)
                i += 1

    # Met à jour le patch de cout minimum de la colonne j
    def update_memo_min(self, patch, j):
        if min(self.memo_min[j].cost, patch.cost) == patch.cost:
            self.memo_min[j] = patch

    # Calcule le patch de cout minimum en fonction des différents couts,
    # et ajoute ce patch au tableau au memo
    def min_and_add_atom(self, id_cost, s_cost, d_cost, md_cost, a_cost, i, j):
        # La multi-destruction ne s'applique que si le nombre de lignes
        # à détruire est >= 2
        i_min = self.memo_min[j].lines_in
        if (i - i_min) < 2:
            md_cost = INFINITY

        # On recherche le cout minimum
        min_cost = min(id_cost, s_cost, d_cost, md_cost, a_cost)

        # Calcul du patch (i,j) a partir d'un patch précédent
        if min_cost == s_cost:
            line = self.file_after_patch[j-1]
            patch = self.memo_prec[j - 1].copy_and_add(SubstituteAtom(i, line))
        elif min_cost == d_cost:
            patch = self.memo_prec[j].copy_and_add(DestructionAtom(i))
        elif min_cost == md_cost:
            nb_del = i - i_min  # nombre de suppressions
            line_nb = i_min + 1  # ligne du début de la supression
            patch = self.memo_min[j].copy_and_add(DestructionMultAtom(line_nb, nb_del))
        elif min_cost == a_cost:
            line = self.file_after_patch[j-1]
            patch = self.memo_cur[j - 1].copy_and_add(AdditionAtom(i, line))
        else:
            patch = self.memo_prec[j - 1].copy()
            patch.lines_in += 1
            patch.lines_out += 1

        # Ajout du patch (i,j) dans la liste
        self.memo_cur.append(patch)
        # Mise à jour de la liste des minimum
        self.update_memo_min(patch, j)

    def compute_patch_opt(self):
        # Cas spéciaux pour 0 ou 1 lignes
        if self.nb_line_n1 == 0:
            return self.memo_prec[self.nb_line_n2]
        elif self.nb_line_n2 == 0:
            if self.nb_line_n1 == 1:
                return Patch(DestructionAtom(1))
            else:
                return Patch(DestructionMultAtom(1, self.nb_line_n1))

        # Parcours des lignes de chaque fichier
        for i in range(1, self.nb_line_n1 + 1):

            self.memo_cur = []
            if i == 1:
                p = Patch(DestructionAtom(1))
            else:
                p = Patch(DestructionMultAtom(1, i))
            p.lines_in = i
            self.memo_cur.append(p)

            for j in range(1, self.nb_line_n2 + 1):

                if self.file_before_patch[i-1] == self.file_after_patch[j-1]:
                    identity_cost = self.memo_prec[j - 1].cost
                else:
                    identity_cost = INFINITY

                sub_cost = self.memo_prec[j - 1].cost + 11 + len(self.file_after_patch[j-1])
                simple_del_cost = self.memo_prec[j].cost + 10
                mult_del_cost = self.memo_min[j].cost + 15
                add_cost = self.memo_cur[j - 1].cost + 11 + len(self.file_after_patch[j-1])

                # Calcul du minimum et sauvegarde dans le tableau
                self.min_and_add_atom(identity_cost,
                                      sub_cost,
                                      simple_del_cost,
                                      mult_del_cost,
                                      add_cost,
                                      i,
                                      j)

            self.memo_prec = self.memo_cur

        return self.memo_prec[self.nb_line_n2]

if __name__ == '__main__': # permet d'importer le fichier sans exécuter ce qui suit
    if len(sys.argv) != 3:
        print('Syntax: %s <source file> <target file>' % sys.argv[0])
        sys.exit(1)

    # Lecture des paramêtres en entrée et ouverture des fichiers
    f1 = open(sys.argv[1], "r")
    f2 = open(sys.argv[2], "r")
    file_before_patch = f1.readlines()
    file_after_patch = f2.readlines()

    # Creation des conditions initiales a partir du ficher
    a = TabPatch(file_before_patch,file_after_patch)
    # Calcul du patch de cout minimum
    patch = a.compute_patch_opt()
    # Affichage du cout et du patch
    print(patch.cost, file=sys.stderr) # permet de filtrer la sortie, pour ne conserver que le score ou que le patch
    print(patch)
