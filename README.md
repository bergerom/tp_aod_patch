# Génération de patch optimal

Matthieu Bergeron, Tom Cornebize

L'exécution du code de ce projet nécessite Python 3.

Toutes les commandes ci-dessous supposent que le répertoire courant est à la racine
du dossier du projet.

## Génération d'un patch

Un patch pour deux fichiers f_in et f_out peut être généré avec la commande suivante.

    ./computepatch_src/ComputePatch.py f_in f_out


On peut également afficher le coût de ce patch (sur stderr) avec la commande suivante.

    ./computepatch_src/ComputePatch.py f_in f_out -c


## Outils annexes

Des tests unitaires accompagnent ce programme. Pour les exécuter, utiliser la commande
suivante.

    ./computepatch_src/Test.py

Un programme de génération de fichiers de test est également présent. Il prend en
entrée une taille de fichier, génère aléatoirement un fichier f_in de cette taille,
puis créé une copie aléatoirement modifiée de f_in : f_out. Chacune de ces modifications
est une modification de notre problème (substitution, addition, destruction, destruction
multiple). On a donc une borne supérieure sur le coût du patch transformant f_in
en f_out. La taille de f_out n'est pas nécessairement égale à la taille de f_in,
mais elle est en général relativement proche.
On peut générer ces deux fichiers (avec f_in de taille 100) avec la commande suivante.

    ./benchmark_generator.py f_in f_out 100

On peut vérifier que le patch calculé est correct en utilisant applyPatch. Pour cela,
commencer par compiler ce programme avec la commande suivante.

    make binary

Puis utiliser la commande suivante, pour deux fichiers f_in et f_out.

    ./verifier.sh f_in f_out

On peut également faire une verification plus poussée de notre programme, en vérifiant
également que le coût du patch calculé est cohérent. Pour cela, utiliser la commande
suivante, qui génère deux fichiers aléatoirement en utilisant benchmark_generator.py,
vérifie la correction du patch avec verifier.sh puis compare le coût du patch
avec la borne donnée par benchmark_generator.py (f_in est toujours de taille 100).

    ./correctionTester.sh 100

Enfin, on peut mesurer le temps d'exécution de notre programme sur deux fichiers
générés aléatoirement (f_in est toujours de taille 100) avec la commande suivante.
La correction des patch n'est pas vérifiée ici.

    ./chronometer.sh 100
