from PatchAtom import *
from Patch import *
import sys

class TabPatch:

    def __init__(self):
        if len(sys.argv) == 3:
            f1 = open(sys.argv[1], "r")
            f2 = open(sys.argv[2], "r")

            self.file_before_patch = f1.readlines()
            self.file_after_patch = f2.readlines()
            self.nb_line_n1 = len(self.file_before_patch)
            self.nb_line_n2 = len(self.file_after_patch)

            # Tableau de mémorisation
            self.memo = []
            for i in range(0, self.nb_line_n1):
                self.memo.append([])

            # Conditions initiales
            patch_00 = Patch()
            patch_10 = patch_00
            patch_01 = Patch()
            first_line = self.file_after_patch.pop(0)
            patch_01.add_atom(AdditionAtom(0, first_line))
            self.memo[0].append(patch_00)
            self.memo[0].append(patch_01)
            self.memo[1].append(patch_10)


