#!/usr/bin/env bash

# Prend en argument une taille de fichier.
# Génère aléatoirement deux fichiers de la taille donnée, génère le patch correspondant,
# puis vérifie sa correction (patch correct, et de coût inférieur à la borne trouvée
# par le générateur).

FILE_IN="/tmp/infile"
FILE_OUT="/tmp/outfile"

if [ $# -ne 1 ] ; then
    echo "Syntax:" $0 "<file size>"
    exit 1
fi

COST_BOUND=`./benchmark_generator.py $FILE_IN $FILE_OUT $1`
if [ $? -ne 0 ] ; then
    echo "Error with benchmark_generator."
    exit 1
fi

OPTIMAL_COST=`./verifier.sh $FILE_IN $FILE_OUT 2>&1`
if [ $? -ne 0 ] ; then
    echo "Error with verifier."
    exit 1
fi

if [ $COST_BOUND -lt $OPTIMAL_COST ] ; then
    echo "Non optimal cost."
    echo "Expected <= " $COST_BOUND
    echo "Got " $OPTIMAL_COST
    exit 1
fi
