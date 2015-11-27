#!/usr/bin/env python3

import sys
import random
import string

# Génère deux fichiers aléatoirement, le second étant une copie modifiée du premier.

class Generator:

    def __init__(self):
        self.cost = 0

    @staticmethod
    def random_string(size=10):
       return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    @classmethod
    def generate_infile(cls, size=None):
        if size is None:
            size = random.randint(50, 100)
        f = []
        for _ in range(size):
            f.append(cls.random_string(random.randint(1, 20)))
        return f

    def generate_outfile(self, infile):
        '''
            Renvoie une copie du fichier d'entrée qui a été aléatoirement modifiée.
        '''
        outfile = list(infile)
        for i in range(len(infile)):
            operation = random.randint(0, 100)
            if(operation < 80): # on ne fait rien dans 80% des cas
                continue
            possible_operations = [self.substitution, self.addition, self.deletion, self.multideletion]
            try:
                possible_operations[operation%len(possible_operations)](outfile, i)
            except IndexError: # on a supprimé trop de lignes
                break
        return outfile

    def substitution(self, outfile, line_number):
        string = self.random_string()
        self.cost += 10 + len(string) + 1
        outfile[line_number] = string

    def addition(self, outfile, line_number):
        string = self.random_string()
        self.cost += 10 + len(string) + 1
        outfile[line_number:line_number] = [string]

    def deletion(self, outfile, line_number):
        self.cost += 10
        outfile[line_number:line_number+1] = []

    def multideletion(self, outfile, line_number):
        self.cost += 15
        outfile[line_number:random.randint(2, 10)] = []

def write_file(file_name, string_list):
    with open(file_name, 'w') as f:
        for line in string_list:
            print(line, file=f)

def help() :
    print('Syntax: %s <source file> <target file> <source file size>' % sys.argv[0])
    sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        help()
    try:
        file_size = int(sys.argv[3])
    except ValueError:
        help()
    generator = Generator()
    infile = generator.generate_infile(file_size)
    outfile = generator.generate_outfile(infile)
    write_file(sys.argv[1], infile)
    write_file(sys.argv[2], outfile)
    print(generator.cost)
