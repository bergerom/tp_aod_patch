#!/usr/bin/env bash

FILE_IN="/tmp/infile"
FILE_OUT="/tmp/outfile"

if [ $# -ne 1 ] ; then
    echo "Syntax:" $0 "<file size>"
    exit 1
fi

./benchmark_generator.py $FILE_IN $FILE_OUT $1 > /dev/null
if [ $? -ne 0 ] ; then
    echo "Error with benchmark_generator."
    exit 1
fi

time ./computepatch_src/ComputePatch.py $FILE_IN $FILE_OUT > /dev/null
if [ $? -ne 0 ] ; then
    echo "Error with computePatch."
    exit 1
fi
