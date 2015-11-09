from PatchAtom import *
from Patch import *

# Script simple pour tester le type patch sur l'exemple de l'ennoncé
a = AdditionAtom(0, "@#?!")
b = AdditionAtom(1, "u")
c = SubstituteAtom(3, "v")
d = DestructionMultAtom(4, 2)
e = AdditionAtom(6, "ww")

p = Patch()
p.add_atom(a)
p.add_atom(b)
p.add_atom(c)
p.add_atom(d)
p.add_atom(e)

print(p)
print("Cout total du patch : {}".format(p.cost))