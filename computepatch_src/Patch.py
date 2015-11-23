import copy
from PatchAtom import *


class Patch:
    def __init__(self, patch_atom=None):
        super().__init__()
        self.atom_list = []
        self.cost = 0
        self.lines_in = 0
        self.lines_out = 0
        if patch_atom is not None:
            self.add_atom(patch_atom)

    def __str__(self):
        s = ""
        for a in self.atom_list:
            s += str(a)
        return s

    # Retourne une copie du patch
    def copy(self):
        copy_patch = Patch()
        copy_patch.atom_list = copy.copy(self.atom_list)
        copy_patch.cost = copy.copy(self.cost)
        copy_patch.lines_in = copy.copy(self.lines_in)
        copy_patch.lines_out = copy.copy(self.lines_out)
        return copy_patch

    # Retourne une copie du patch avec une nouvelle instruction
    def copy_and_add(self, next_atom):
        copy_patch = self.copy()
        copy_patch.add_atom(next_atom)
        return copy_patch

    # Ajoute une instruction à la liste
    def add_atom(self, atom):
        self.atom_list.append(atom)
        self.cost += atom.compute_cost()
        i, j = atom.update_line_nb()
        self.lines_in += i
        self.lines_out += j
