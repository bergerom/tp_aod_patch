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

    @abstractmethod
    def update_line_nb(self):
        pass


# Classes héritant de PatchAtom

class AdditionAtom(PatchAtom):
    def update_line_nb(self):
        return 0, 1

    def __init__(self, line_nb, new_line):
        super().__init__(line_nb)
        self.new_line = new_line

    def __str__(self):
        return "+ {}\n{}".format(self.line_number, self.new_line)

    def compute_cost(self):
        return 10 + len(self.new_line)


class SubstituteAtom(PatchAtom):
    def update_line_nb(self):
        return 1, 1

    def __init__(self, line_nb, subs_line):
        super().__init__(line_nb)
        self.subs_line = subs_line

    def __str__(self):
        return "= {}\n{}".format(self.line_number, self.subs_line)

    def compute_cost(self):
        return 10 + len(self.subs_line)


class DestructionAtom(PatchAtom):
    def update_line_nb(self):
        return 1, 0

    def __str__(self):
        return "d {}\n".format(self.line_number)

    def compute_cost(self):
        return 10


class DestructionMultAtom(PatchAtom):
    def update_line_nb(self):
        return self.destruction_nb, 0

    def __init__(self, line_nb, destruction_nb):
        super().__init__(line_nb)
        self.destruction_nb = destruction_nb

    def __str__(self):
        return "D {} {}\n".format(self.line_number, self.destruction_nb)

    def compute_cost(self):
        return 15
