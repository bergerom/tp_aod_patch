from abc import ABCMeta, abstractmethod

# Classe abstraite Parent

class PatchAtom:
    def __init__(self, line_nb):
        self.line_number = line_nb

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.line_number)

# Classes héritant de PatchAtom

class AdditionAtom(PatchAtom):
    def __init__(self, line_nb, new_line):
        super().__init__(line_nb)
        assert isinstance(new_line, str)
        self.new_line = new_line
        self.cost = 10 + len(self.new_line)

    def __str__(self):
        return "+ {}\n{}".format(self.line_number, self.new_line.replace('\n', ''))

    @staticmethod
    def compute_cost(line):
        return 10 + len(line)

class SubstituteAtom(PatchAtom):
    def __init__(self, line_nb, subs_line):
        super().__init__(line_nb)
        assert isinstance(subs_line, str)
        self.subs_line = subs_line
        self.cost = 10 + len(self.subs_line)

    def __str__(self):
        return "= {}\n{}".format(self.line_number, self.subs_line.replace('\n', ''))

    @staticmethod
    def compute_cost(line):
        return 10 + len(line)

class DestructionAtom(PatchAtom):
    cost = 10
    def __init__(self, line_nb):
        super().__init__(line_nb)

    def __str__(self):
        return "d {}".format(self.line_number)

    @staticmethod
    def compute_cost():
        return 10

class DestructionMultAtom(PatchAtom):
    cost = 15
    def __init__(self, line_nb, destruction_nb):
        super().__init__(line_nb)
        self.destruction_nb = destruction_nb

    def __str__(self):
        return "D {} {}".format(self.line_number, self.destruction_nb)

    @staticmethod
    def compute_cost():
        return 15
