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
        self.current_patch[0] = Patch(Patch(), AdditionAtom(0, self.file_out[1]))
        self.previous_patch[0] = Patch()
        self.previous_patch[1] = Patch(self.previous_patch[0], DestructionAtom(1))
        for i in range(1, len(self.file_in)):
            self.previous_patch[i] = Patch(self.previous_patch[0], DestructionMultAtom(1, i))

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
                self.current_patch[0] = Patch(self.previous_patch[0], AdditionAtom(0, self.file_out[index_out+1]))
        return self.current_patch[-1]

    def speciale_cases(self):
        patch = None
        if self.file_in[1:] == []:
            patch = Patch()
            for line in self.file_out[1:]:
                patch = Patch(patch, AdditionAtom(0, line))
        elif self.file_out[1:] == []:
            patch = Patch()
            if len(self.file_in[1:]) == 1:
                patch = Patch(patch, DestructionAtom(1))
            else:
                patch = Patch(patch, DestructionMultAtom(1, len(self.file_in[1:])))
        return patch

    def compute_at_indexes(self, index_in, index_out):
        '''
            Méthode moche, avec beaucoup de valeurs codées en dur (ce qui a permis
            de diviser son temps d'exécution par 2).
        '''
        possible_costs = []
        if self.file_in[index_in] == self.file_out[index_out]:
            identity_cost = self.previous_patch[index_in-1].cost
            possible_costs.append(identity_cost)
        else:
            identity_cost = INFINITY
        substitute_cost = self.previous_patch[index_in-1].cost + 10 + len(self.file_out[index_out])
        possible_costs.append(substitute_cost)
        addition_cost = self.previous_patch[index_in].cost + 10 + len(self.file_out[index_out])
        possible_costs.append(addition_cost)
        destruction_cost = self.current_patch[index_in-1].cost + 10
        possible_costs.append(destruction_cost)
        size = index_in - self.min_current_index
        if self.min_current_index < index_in-1:
            destructionMult_cost = self.current_patch[self.min_current_index].cost + 15
            possible_costs.append(destructionMult_cost)
        else:
            destructionMult_cost = INFINITY
        minimal_cost = min(possible_costs)
        if minimal_cost == identity_cost :
            self.current_patch[index_in] = Patch(self.previous_patch[index_in-1], IdentityAtom(index_in))
        elif minimal_cost == substitute_cost:
            self.current_patch[index_in] = Patch(self.previous_patch[index_in-1], SubstituteAtom(index_in, self.file_out[index_out]))
        elif minimal_cost == addition_cost:
            self.current_patch[index_in] = Patch(self.previous_patch[index_in], AdditionAtom(index_in, self.file_out[index_out]))
        elif minimal_cost == destruction_cost:
            self.current_patch[index_in] = Patch(self.current_patch[index_in-1], DestructionAtom(index_in))
        else:
            assert minimal_cost == destructionMult_cost
            self.current_patch[index_in] = Patch(self.current_patch[self.min_current_index], DestructionMultAtom(self.min_current_index+1, size))
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
    print("%d" % patch.cost, file=sys.stderr)
    print(patch)
