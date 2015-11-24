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
            patch.add_atom(atom)
        self.assertEqual(sum(atom.compute_cost() for atom in atoms), patch.cost)
        self.assertEqual(sum(atom.update_line_nb()[0] for atom in atoms), patch.lines_in)
        self.assertEqual(sum(atom.update_line_nb()[1] for atom in atoms), patch.lines_out)


    def testPatchCopy(self):
        patch = Patch()
        patch.add_atom(AdditionAtom(3, 'xyz'))
        patch.add_atom(DestructionAtom(6))
        patch.add_atom(SubstituteAtom(8, 'foo'))
        patch2 = patch.copy()
        self.assertIsNot(patch, patch2)
        self.assertEqual(patch, patch2)
        atom = SubstituteAtom(9, 'bar')
        patch2.add_atom(atom)
        self.assertNotEqual(patch, patch2)
        self.assertEqual(3, len(patch.atom_list))
        self.assertEqual(4, len(patch2.atom_list))
        patch.add_atom(atom)
        self.assertEqual(patch, patch2)
