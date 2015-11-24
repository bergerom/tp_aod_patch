from PatchAtom import *


class Patch:
    def __init__(self, patch_atom=None):
        self.atom_list = []
        self.cost = 0
        self.lines_in = 0
        self.lines_out = 0
        if patch_atom is not None:
            self.add_atom(patch_atom)

    def __str__(self):
        return "\n".join(str(atom) for atom in self.atom_list if not isinstance(atom, IdentityAtom))

    def __lt__(self, other):
        assert(isinstance(other, self.__class__))
        return self.cost < other.cost

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    # Retourne une copie du patch
    def copy(self):
        copy_patch = Patch()
        copy_patch.atom_list = list(self.atom_list) # copie de la liste, mais avec contenu partagé
        copy_patch.cost = self.cost
        copy_patch.lines_in = self.lines_in
        copy_patch.lines_out = self.lines_out
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
