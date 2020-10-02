#!/bin/bash

# Runs benchmark tests on all distances
for i in "levenshtein" "levenshtein2" "jarowinkler" "hamming"
do
    cat data/devoir3-train.txt | cut -f 1 | python correction.py data/voc-1bwc.txt \
        --time --$i > $i.txt
done