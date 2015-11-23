import unittest
from PatchAtom import *
from Patch import *

class TestPatch(unittest.TestCase):
    def testPatchInitialisation(self):
        self.fail("Not implemented.") # TODO

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
