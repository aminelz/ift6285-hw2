#!/bin/bash

# Downloads the text data for testing the program, if needed
if [ ! -d "data" ]; then
    mkdir data
fi

voc="data/voc-1bwc.txt"
train="data/devoir3-train.txt"
if [ ! -f "data/voc-1bwc.txt" ]; then
    curl "http://www-labs.iro.umontreal.ca/~felipe/IFT6285-Automne2020/voc-1bwc.txt" \
        -o $voc
fi
if [ ! -f "data/devoir3-train.txt" ]; then
    curl "http://www-labs.iro.umontreal.ca/~felipe/IFT6285-Automne2020/devoir3-train.txt" \
        -o $train
fi
