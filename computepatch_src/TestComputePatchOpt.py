import unittest
import random
import string
import copy
from PatchAtom import *
from Patch import *
from ComputePatch import *

def random_string(size):
   return ''.join(random.choice(string.ascii_letters) for _ in range(size))

def generate_file(size=None):
    if size is None:
        size = random.randint(50, 100)
    f = []
    for _ in range(size):
        f.append(random_string(random.randint(1, 20)))
    return f

class TestTrivialComputePatch(unittest.TestCase):

    def testSameFiles(self):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        self.assertEqual(0, patch.cost)
        self.assertEqual("", str(patch))

    def testEmptyInFile(self):
        f_in = []
        f_out = generate_file()
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        for string in f_out:
            self.assertIn(AdditionAtom(0, string), patch.atom_list)

    def testEmptyOutFile(self):
        f_in = generate_file()
        f_out = []
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        self.assertEqual(1, len(patch.atom_list))
        atom = patch.atom_list[0]
        self.assertEqual(DestructionMultAtom(1, len(f_in)), atom)

class TestGeneralComputePatch(unittest.TestCase):

    def testSubstitution(self, begin=None, end=None):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        begin = begin or random.randint(len(f_out)//4, len(f_out)//2)
        end = end or random.randint(begin+1, 3*len(f_out)//4)
        if end == -1:
            end = len(f_in)-1
        for i in range(begin, end):
            f_out[i] = f_out[i] + '@'
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = patch.atom_list
        self.assertEqual(end-begin, len(atoms))
        for i in range(begin, end):
            self.assertIn(SubstituteAtom(i+1, f_out[i]), atoms) # ligne=i+1 car on indice les lignes à partir de 1 dans l'algorithme

    def testSubstitutionBegin(self):
        self.testSubstitution(begin=0)

    def testSubstitutionEnd(self):
        self.testSubstitution(end=-1)

    def testAddition(self, position=None):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        position = position or random.randint(0, len(f_out))
        if position==-1:
            position = len(f_in)-1
        size = random.randint(0, 10)
        f_out[position:position] = ['@']*size
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = patch.atom_list
        self.assertEqual(size, len(atoms))
        for i in range(position, position+size):
            self.assertIn(AdditionAtom(position, f_out[i]), atoms)

    def testAdditionBegin(self):
        self.testAddition(0)

    def testAdditionEnd(self):
        self.testAddition(-1)

    def testDestruction(self, position=None):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        position = position or random.randint(len(f_out)//4, 3*len(f_out)//4)
        if position == -1:
            position = len(f_in)-1
            f_out[-1:] = []
        else:
            f_out[position:position+1] = []
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = patch.atom_list
        self.assertEqual(1, len(atoms))
        self.assertEqual(DestructionAtom(position+1), atoms[0])

    def testDestructionBegin(self):
        self.testDestruction(0)

    def testDestructionEnd(self):
        self.testDestruction(-1)

    def testDestructionMult(self, begin=None, end=None):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        begin = begin or random.randint(len(f_out)//4, len(f_out)//2)
        end = end or random.randint(begin+2, 3*len(f_out)//4)
        if end == -1:
            end = len(f_in)-1
        f_out[begin:end] = []
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = patch.atom_list
        self.assertEqual(1, len(atoms))
        self.assertEqual(DestructionMultAtom(begin+1, end-begin), atoms[0])

    def testDestructionMultBegin(self):
        self.testDestructionMult(begin=0)

    def testDestructionMultEnd(self):
        self.testDestructionMult(end=-1)
