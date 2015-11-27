#!/usr/bin/env bash

PATCH_LOCATION="/tmp/patch"
OUT_LOCATION="/tmp/out"

if [ $# -ne 2 ] ; then
    echo "Syntax:" $0 "<file_in> <file_out>"
    exit 1
fi

./computepatch_src/ComputePatch.py $1 $2 1> $PATCH_LOCATION
if [ $? -ne 0 ] ; then
    echo "Error with computePatch."
    exit 1
fi

./bin/applyPatch $PATCH_LOCATION $1 > $OUT_LOCATION
if [ $? -ne 0 ] ; then
    echo "Error with applyPatch."
    exit 1
fi

diff $2 $OUT_LOCATION
if [ $? -ne 0 ] ; then
    echo "Error, different files."
    exit 1
fi
