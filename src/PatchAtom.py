from abc import ABCMeta, abstractmethod

# Ce fichier contient la classe PatchAtom et ses dérivées. Chaque instance d'une
# de ces classes représente une opération d'un patch (par exemple, ue substitution).

class PatchAtom:
    '''
        Classe abstraite, mère de toutes les autres classes.
    '''
    def __init__(self, line_nb):
        self.line_number = line_nb

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.line_number)

# Classes héritant de PatchAtom

class AdditionAtom(PatchAtom):
    '''
        Addition de la chaîne new_line en position line_nb.
    '''
    def __init__(self, line_nb, new_line):
        super().__init__(line_nb)
        assert isinstance(new_line, str)
        self.new_line = new_line
        self.cost = 10 + len(self.new_line)

    def __str__(self):
        return "+ {}\n{}".format(self.line_number, self.new_line.replace('\n', ''))

class SubstituteAtom(PatchAtom):
    '''
        Substitution de la chaîne de position line_nb par la chaîne subs_line.
    '''
    def __init__(self, line_nb, subs_line):
        super().__init__(line_nb)
        assert isinstance(subs_line, str)
        self.subs_line = subs_line
        self.cost = 10 + len(self.subs_line)

    def __str__(self):
        return "= {}\n{}".format(self.line_number, self.subs_line.replace('\n', ''))

class DestructionAtom(PatchAtom):
    '''
        Destruction de la chaîne de position line_nb.
    '''
    cost = 10
    def __init__(self, line_nb):
        super().__init__(line_nb)

    def __str__(self):
        return "d {}".format(self.line_number)

class DestructionMultAtom(PatchAtom):
    '''
        Destruction de destruction_nb chaînes à partir de la position line_nb.
    '''
    cost = 15
    def __init__(self, line_nb, destruction_nb):
        super().__init__(line_nb)
        self.destruction_nb = destruction_nb

    def __str__(self):
        return "D {} {}".format(self.line_number, self.destruction_nb)
