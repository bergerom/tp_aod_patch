import unittest
import random
import string
import copy
from PatchAtom import *
from Patch import *
from ComputePatchOpt import *

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
        self.assertEqual([], patch.atom_list)

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
