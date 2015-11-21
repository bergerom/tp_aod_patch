# Classe qui calcule le patch de cout minimal
# Utilisation : python ComputePatchOpt fichier1 fichier2
from PatchAtom import *
from Patch import *
import sys

class TabPatch:
    def __init__(self):
        if len(sys.argv) == 3:
            f1 = open(sys.argv[1], "r")
            f2 = open(sys.argv[2], "r")

            self.file_before_patch = f1.readlines()
            self.file_after_patch = f2.readlines()
            self.nb_line_n1 = len(self.file_before_patch)
            self.nb_line_n2 = len(self.file_after_patch)

            # Conditions limites
            self.memo_min = []
            p = Patch()
            p.cost = 1000000
            for line in range(0, self.nb_line_n2 + 1):
                self.memo_min.append(p)

            self.memo_cur = []

            self.memo_prec = []
            i = 0
            p = Patch()
            self.memo_prec.append(p)
            for line in self.file_after_patch:
                p = p.copy_and_add(AdditionAtom(i, line))
                self.memo_prec.append(p)
                i += 1

    # Calcule le patch de cout minimum en fonction des différents couts,
    # et ajoute ce patch au tableau au memo
    def min_and_add_atom(self, id_cost, s_cost, d_cost, md_cost, a_cost, i, j):
        min_cost = min(id_cost, s_cost, d_cost, md_cost, a_cost)
        # Calcul du patch (i,j)
        if min_cost == s_cost:
            line = self.file_after_patch[j-1]
            patch = self.memo_prec[j - 1].copy_and_add(SubstituteAtom(i, line))
        elif min_cost == d_cost:
            patch = self.memo_prec[j].copy_and_add(DestructionAtom(i))
        elif min_cost == md_cost:
            line_nb = self.memo_min[j-1].lines_out
            nb_del = i - line_nb - 1 # nombre de suppressions
            patch = self.memo_min[j].copy_and_add(DestructionMultAtom(line_nb + 1, nb_del))
        elif min_cost == a_cost:
            line = self.file_after_patch[j-1]
            patch = self.memo_cur[j - 1].copy_and_add(AdditionAtom(j-1, line))
        else:
            patch = self.memo_prec[j - 1].copy()

        # Ajout du patch (i,j) dans la liste
        self.memo_cur.append(patch)
        # Mise à jour de la liste des minimum
        print("({},{})".format(i, j))
        print(patch)
        print("-------------------")
        self.update_memo_min(patch, i)

    # Met à jour le cout minimum de chaque colonne
    def update_memo_min(self, patch, i):
        if min(self.memo_min[i].cost, patch.cost) == patch.cost:
            self.memo_min[i] = patch

    def compute_patch_opt(self):
        if self.nb_line_n1 == 0:
            return self.memo_prec[self.nb_line_n2]
        elif self.nb_line_n2 == 0:
            if self.nb_line_n1 == 1:
                return Patch(DestructionAtom(1))
            else:
                return Patch(DestructionMultAtom(1, self.nb_line_n2))

        for i in range(1, self.nb_line_n1 + 1):

            self.memo_cur = []
            if i == 1:
                self.memo_cur.append(Patch(DestructionAtom(0)))
            else:
                self.memo_cur.append(Patch(DestructionMultAtom(0, i)))

            for j in range(1, self.nb_line_n2 + 1):

                if self.file_before_patch[i-1] == self.file_after_patch[j-1]:
                    identity_cost = self.memo_prec[j - 1].cost
                else:
                    identity_cost = 1000000

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

            self.memo_prec = self.memo_cur.copy()

        return self.memo_prec[self.nb_line_n2]


# Creation des conditions initiales a partir du ficher
a = TabPatch()
# Calcul du patch de cout minimum
b = a.compute_patch_opt()
# Affichage du cout et du patch
print(b.cost)
print(b)
