import unittest
import random
from PatchAtom import *
from Patch import *

class TestPatch(unittest.TestCase):

    def testPatchInitialisation(self):
        atom_classes = [SubstituteAtom, AdditionAtom, DestructionAtom, DestructionMultAtom]
        atoms = []
        patch = Patch()
        patch_size = 100
        line_nb = 0
        for _ in range(patch_size):
            atom_class = random.choice(atom_classes)
            if(atom_class in {SubstituteAtom, AdditionAtom}):
                atom = atom_class(line_nb, 'a'*random.randint(1, 20))
            elif(atom_class is DestructionAtom):
                atom = atom_class(line_nb)
            else: # DestructionMultAtom
                size = random.randint(2, 10)
                atom = atom_class(line_nb, size)
                line_nb += size
            line_nb += random.randint(1, 10)
            atoms.append(atom)
            patch = Patch(patch, atom)
        self.assertEqual(sum(atom.compute_cost() for atom in atoms), patch.cost)
