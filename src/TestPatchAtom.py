import unittest
import random
from PatchAtom import *
from Patch import *

class TestPatchAtom(unittest.TestCase):

    def verify_patch(self, atom, expected_cost, expected_line_number):
        self.assertEqual(expected_cost, atom.cost)
        self.assertEqual(expected_line_number, atom.line_number)

    def test_patch_AdditionAtom(self):
        line_number = random.randint(0, 10)
        string_length = random.randint(0, 20)
        atom = AdditionAtom(line_number, 'a'*string_length)
        self.verify_patch(atom, 10+string_length, line_number)

    def test_patch_AubstitutionAtom(self):
        line_number = random.randint(0, 10)
        string_length = random.randint(0, 20)
        atom = SubstituteAtom(line_number, 'a'*string_length)
        self.verify_patch(atom, 10+string_length, line_number)

    def test_patch_AestructionAtom(self):
        line_number = random.randint(0, 10)
        atom = DestructionAtom(line_number)
        self.verify_patch(atom, 10, line_number)

    def test_patch_DestructionMultAtom(self):
        line_number = random.randint(0, 10)
        destruction_size = random.randint(5, 10)
        atom = DestructionMultAtom(line_number, destruction_size)
        self.verify_patch(atom, 15, line_number)

    def test_equal(self):
        line = random.randint(0, 10)
        destruction_size = random.randint(0, 10)
        string = 'a'*random.randint(0, 20)
        for atom_class in [AdditionAtom, SubstituteAtom]:
            self.assertEqual(atom_class(line, string), atom_class(line, str(string)))
            self.assertNotEqual(atom_class(line, string), atom_class(line+1, str(string)))
            self.assertNotEqual(atom_class(line, string), atom_class(line, string+'b'))
        self.assertEqual(DestructionAtom(line), DestructionAtom(line))
        self.assertNotEqual(DestructionAtom(line), DestructionAtom(line+1))
        self.assertEqual(DestructionMultAtom(line, destruction_size), DestructionMultAtom(line, destruction_size))
        self.assertNotEqual(DestructionMultAtom(line, destruction_size), DestructionMultAtom(line+1, destruction_size))
        self.assertNotEqual(DestructionMultAtom(line, destruction_size), DestructionMultAtom(line, destruction_size+1))
        atoms = [AdditionAtom(line, string), SubstituteAtom(line, string), DestructionAtom(line), DestructionMultAtom(line, destruction_size)]
        for a1 in atoms:
            for a2 in atoms:
                if type(a1) != type(a2):
                    self.assertNotEqual(a1, a2)
