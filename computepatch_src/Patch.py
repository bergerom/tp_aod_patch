from PatchAtom import *


class Patch:
    def __init__(self, previous_patch=None, patch_atom=None):
        self.cost = 0
        self.patch_atom = patch_atom
        self.previous_patch = previous_patch
        if previous_patch is not None:
            assert patch_atom is not None
            self.cost = previous_patch.cost + patch_atom.compute_cost()

    def __str__(self):
        return "\n".join(str(atom) for atom in self.atom_list if not isinstance(atom, IdentityAtom))

    def __repr__(self):
        return str(self)

    def __lt__(self, other):
        assert(isinstance(other, self.__class__))
        return self.cost < other.cost

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    @property
    def atom_list(self):
        atom_list = []
        patch = self
        while patch.patch_atom is not None:
            atom_list.append(patch.patch_atom)
            patch = patch.previous_patch
        atom_list.reverse()
        return atom_list
