from abc import ABCMeta, abstractmethod

# Classe abstraite Parent

class PatchAtom:
    def __init__(self, line_nb):
        self.line_number = line_nb

    def __eq__(self, other):
        return type(other) is type(self) and self.__dict__ == other.__dict__

    def __repr__(self):
        return '%s(%d)' % (self.__class__.__name__, self.line_number)

    @abstractmethod
    def compute_cost(self):
        pass


# Classes héritant de PatchAtom

class IdentityAtom(PatchAtom):
    def __str__(self):
        return ""

    def compute_cost(self):
        return 0

class AdditionAtom(PatchAtom):
    def __init__(self, line_nb, new_line):
        super().__init__(line_nb)
        assert isinstance(new_line, str)
        self.new_line = new_line

    def __str__(self):
        return "+ {}\n{}".format(self.line_number, self.new_line.replace('\n', ''))

    def compute_cost(self):
        return 10 + len(self.new_line)


class SubstituteAtom(PatchAtom):
    def __init__(self, line_nb, subs_line):
        super().__init__(line_nb)
        assert isinstance(subs_line, str)
        self.subs_line = subs_line

    def __str__(self):
        return "= {}\n{}".format(self.line_number, self.subs_line.replace('\n', ''))

    def compute_cost(self):
        return 10 + len(self.subs_line)


class DestructionAtom(PatchAtom):
    def __str__(self):
        return "d {}".format(self.line_number)

    def compute_cost(self):
        return 10


class DestructionMultAtom(PatchAtom):
    def __init__(self, line_nb, destruction_nb):
        super().__init__(line_nb)
        self.destruction_nb = destruction_nb

    def __str__(self):
        return "D {} {}".format(self.line_number, self.destruction_nb)

    def compute_cost(self):
        return 15
