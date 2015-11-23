import unittest
import random
from PatchAtom import *
from Patch import *

class TestPatchAtom(unittest.TestCase):
    '''
        Vérifie que les PatchAtom sont bien cohérents avec l'énnoncé du sujet.
    '''

    def verify_patch(self, atom, expected_cost, expected_line_number, expected_update_line):
        self.assertEqual(expected_cost, atom.compute_cost())
        self.assertEqual(expected_line_number, atom.line_number)
        self.assertEqual(expected_update_line, atom.update_line_nb())

    def test_patch_AdditionAtom(self):
        line_number = random.randint(0, 10)
        string_length = random.randint(0, 20)
        atom = AdditionAtom(line_number, 'a'*string_length)
        self.verify_patch(atom, 10+string_length, line_number, (0, 1))

    def test_patch_AubstitutionAtom(self):
        line_number = random.randint(0, 10)
        string_length = random.randint(0, 20)
        atom = SubstituteAtom(line_number, 'a'*string_length)
        self.verify_patch(atom, 10+string_length, line_number, (1, 1))

    def test_patch_AestructionAtom(self):
        line_number = random.randint(0, 10)
        atom = DestructionAtom(line_number)
        self.verify_patch(atom, 10, line_number, (1, 0))

    def test_patch_DestructionMultAtom(self):
        line_number = random.randint(0, 10)
        destruction_size = random.randint(5, 10)
        atom = DestructionMultAtom(line_number, destruction_size)
        self.verify_patch(atom, 15, line_number, (destruction_size, 0))
