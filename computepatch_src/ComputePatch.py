#!/usr/bin/env python3

from PatchAtom import *
from Patch import *
from ComputePatchOpt import Infinity

import sys

INFINITY = Infinity()

class TabPatch:
    def __init__(self, file_in, file_out):
        self.file_in = [None]
        self.file_in.extend(file_in) # afin d'avoir un indiçage qui commence à 1
        self.file_out = [None]
        self.file_out.extend(file_out) # afin d'avoir un indiçage qui commence à 1

    def initArrays(self):
        self.previous_patch = [None]*len(self.file_in) # previous_patch[i] = cout(i, j-1) pour j fixé
        self.current_patch = [None]*len(self.file_in)  # current_patch[i]  = cout(i, j)   pour j fixé
        # Initialisation de cout(i, 0) pour tout i
        self.current_patch[0] = self.first_current_patch(1)
        self.previous_patch[0] = Patch()
        self.previous_patch[1] = self.previous_patch[0].copy_and_add(DestructionAtom(1))
        for i in range(1, len(self.file_in)):
            self.previous_patch[i] = self.previous_patch[0].copy_and_add(DestructionMultAtom(1, i))

    def first_current_patch(self, max_line_number):
        patch = Patch()
        for line_number in range(1, max_line_number+1):
            patch.add_atom(AdditionAtom(0, self.file_out[line_number]))
        return patch

    def compute_patch_opt(self):
        special_patch = self.speciale_cases()
        if special_patch is not None:
            return special_patch
        self.initArrays()
        for index_out in range(1, len(self.file_out)):
            self.min_current_index = 0
            for index_in in range(1, len(self.file_in)):
                self.compute_at_indexes(index_in, index_out)
            if index_out < len(self.file_out)-1:
                self.previous_patch = self.current_patch
                self.current_patch = [None]*len(self.file_in)
                self.current_patch[0] = self.first_current_patch(index_out+1)
        return self.current_patch[-1]

    def speciale_cases(self):
        patch = None
        if self.file_in[1:] == []:
            patch = Patch()
            for line in self.file_out[1:]:
                patch.add_atom(AdditionAtom(0, line))
        elif self.file_out[1:] == []:
            patch = Patch()
            if len(self.file_in[1:]) == 1:
                patch.add_atom(DestructionAtom(1))
            else:
                patch.add_atom(DestructionMultAtom(1, len(self.file_in[1:])))
        return patch

    def compute_at_indexes(self, index_in, index_out):
        possible_patches = []
        if self.file_in[index_in] == self.file_out[index_out]:
            possible_patches.append(self.previous_patch[index_in-1].copy_and_add(IdentityAtom(index_in)))
        possible_patches.append(self.previous_patch[index_in-1].copy_and_add(SubstituteAtom(index_in, self.file_out[index_out])))
        possible_patches.append(self.previous_patch[index_in].copy_and_add(AdditionAtom(index_in, self.file_out[index_out])))
        possible_patches.append(self.current_patch[index_in-1].copy_and_add(DestructionAtom(index_in)))
        size = index_in - self.min_current_index
        possible_patches.append(self.current_patch[self.min_current_index].copy_and_add(DestructionMultAtom(self.min_current_index+1, size)))
        self.current_patch[index_in] = min(possible_patches)
        if(self.current_patch[index_in] < self.current_patch[self.min_current_index]):
            self.min_current_index = index_in

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
    patch = TabPatch(file_in, file_out).compute_patch_opt()
    print("cost: %d" % patch.cost)
    print(patch)
