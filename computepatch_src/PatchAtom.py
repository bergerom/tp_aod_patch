from abc import ABCMeta, abstractmethod

# Classe abstraite Parent

class PatchAtom:
    def __init__(self, line_nb):
        self.cost = 0
        self.line_number = 0
        self.line_number = line_nb

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
        return 11 + len(self.new_line)


class SubstituteAtom(PatchAtom):
    def update_line_nb(self):
        return 1, 1

    def __init__(self, line_nb, subs_line):
        super().__init__(line_nb)
        self.subs_line = subs_line

    def __str__(self):
        return "= {}\n{}".format(self.line_number, self.subs_line)

    def compute_cost(self):
        return 11 + len(self.subs_line)


class DestructionAtom(PatchAtom):
    def update_line_nb(self):
        return 1, 0

    def __str__(self):
        return "d {}".format(self.line_number)

    def compute_cost(self):
        return 10


class DestructionMultAtom(PatchAtom):
    def update_line_nb(self):
        return self.destruction_nb, 0

    def __init__(self, line_nb, destruction_nb):
        super().__init__(line_nb)
        self.destruction_nb = destruction_nb

    def __str__(self):
        return "D {} {}".format(self.line_number, self.destruction_nb)

    def compute_cost(self):
        return 15
