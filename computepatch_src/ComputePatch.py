from PatchAtom import *
from Patch import *

import sys

INFINITY = 1000000000

class TabPatch:
    def __init__(self, file_in, file_out):
        self.file_in = [None]
        self.file_in.extend(file_in) # afin d'avoir un indiçage qui commence à 1
        self.file_out = [None]
        self.file_out.extend(file_out) # afin d'avoir un indiçage qui commence à 1
        self.previous_patch = [None]*(len(self.file_in)+1) # previous_patch[i] = cout(i, j-1) pour j fixé
        self.current_patch = [None]*(len(self.file_in)+1)  # current_patch[i]  = cout(i, j)   pour j fixé
        # Initialisation de cout(i, 0) pour tout i
        self.current_patch[0] = self.first_current_patch(1)
        self.previous_patch[0] = Patch()
        self.previous_patch[1] = self.previous_patch[0].copy_and_add(DestructionAtom(1))
        for i in range(len(self.file_in)+1):
            self.previous_patch[i] = self.previous_patch[0].copy_and_add(DestructionMultAtom(1, i))

    def first_current_patch(self, max_line_number):
        patch = Patch()
        for line_number in range(max_line_number):
            patch.add_atom(AdditionAtom(0, self.file_out[line_number]))
        return patch

    def compute(self):
        for index_out in range(1, len(self.file_out)+1):
            for index_in in range(1, len(self.file_in)+1):
                self.computeAtIndexes(index_in, index_out)
            self.previous_patch = self.current_patch
            self.current_patch = [None]*len(self.file_in+1)
            self.current_patch[0] = self.first_current_patch(index_out+1)
        return self.current_patch[-1]

    def computeAtIndexes(self, index_in, index_out):
        possible_patches = []
        if self.file_in[index_in] == self.file_out[index_out]:
            possible_patches.append(self.previous_patch[index_in-1].copy_and_add(IdentityAtom(index_in)))
        possible_patches.append(self.previous_patch[index_in-1].copy_and_add(SubstituteAtom(index_in, self.file_out[index_out])))
        possible_patches.append(self.previous_patch[index_in].copy_and_add(AdditionAtom(index_in, self.file_out[index_out])))
        possible_patches.append(self.current_patch[index_in-1].copy_and_add(DestructionAtom(index_in)))
        optimal_multiple_destruction = min(self.current_patch[:index_in])
        start_line = optimal_multiple_destruction.lines_in
        size = index_in - start_line + 1
        possible_patches.append(optimal_multiple_destruction.copy_and_add(DestructionMultAtom(start_line, size)))
        self.current_patch[index_in] = min(possible_patches)

def help() :
    print('Syntax: %s <source file> <target file>' % sys.argv[0])
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        help()
    with open(sys.argv[1]) as f:
        file_in = f.readlines()
    with open(sys.argv[2]) as f:
        file_out = f.readlines()
    patch = TabPatch(file_in, file_out).compute()
    print("cost: %d" % patch.cost)
    print(patch)
