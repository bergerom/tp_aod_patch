
class Patch:

    def __init__(self):
        self.atom_list = []
        self.cost = 0
        super().__init__()

    def __str__(self):
        s = ""
        for a in self.atom_list:
            s += str(a)
        return s

    # Ajoute une instruction à la liste
    def add_atom(self, atom):
        self.atom_list.append(atom)
        self.cost += atom.compute_cost()
