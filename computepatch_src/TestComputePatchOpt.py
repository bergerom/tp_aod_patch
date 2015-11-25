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

    def testSubstitution(self):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        begin = random.randint(len(f_out)//4, len(f_out)//2)
        end = random.randint(begin+1, 3*len(f_out)//4)
        for i in range(begin, end):
            f_out[i] = f_out[i] + '@'
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = [atom for atom in patch.atom_list if not isinstance(atom, IdentityAtom)]
        self.assertEqual(end-begin, len(atoms))
        for i in range(begin, end):
            self.assertIn(SubstituteAtom(i+1, f_out[i]), atoms) # ligne=i+1 car on indice les lignes à partir de 1 dans l'algorithme

    def testAddition(self):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        position = random.randint(0, len(f_out))
        size = random.randint(0, 10)
        f_out[position:position] = ['@']*size
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = [atom for atom in patch.atom_list if not isinstance(atom, IdentityAtom)]
        self.assertEqual(size, len(atoms))
        for i in range(position, position+size):
            self.assertIn(AdditionAtom(position, f_out[i]), atoms)

    def testDestruction(self):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        begin = random.randint(len(f_out)//4, 3*len(f_out)//4)
        f_out[begin:begin+1] = []
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = [atom for atom in patch.atom_list if not isinstance(atom, IdentityAtom)]
        self.assertEqual(1, len(atoms))
        self.assertEqual(DestructionAtom(begin+1), atoms[0])

    def testDestructionMult(self):
        f_in = generate_file()
        f_out = copy.deepcopy(f_in)
        begin = random.randint(len(f_out)//4, len(f_out)//2)
        end = random.randint(begin+2, 3*len(f_out)//4)
        f_out[begin:end] = []
        patch = TabPatch(f_in, f_out).compute_patch_opt()
        atoms = [atom for atom in patch.atom_list if not isinstance(atom, IdentityAtom)]
        self.assertEqual(1, len(atoms))
        self.assertEqual(DestructionMultAtom(begin+1, end-begin), atoms[0])
