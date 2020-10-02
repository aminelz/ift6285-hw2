#!/bin/bash

# Performs timing on Python scripts

# The output is a one column csv file
# Each line is time in seconds needed to correct one more word on the training corpus
if [ $# -ne 1 ]; then
    echo "Times the execution of an automatic correction model. Time store in a csv file"
    echo "Usage: ./time.sh distance-model"
    echo "Example: ./time.sh levenshtein"
    echo "  A file named time_levenshtein.csv will be generated." 
    exit 1
fi

# check data availability
train="data/devoir3-train.txt"
voc="data/voc-1bwc.txt"
if [ ! -f $train ] || [ ! -f $voc ] ; then
    ./setup.sh
fi

# start the time per line of corpus read
TIMEFORMAT=%R
output_time="time_$1.csv"
> $output_time
limit=100
for ((word_read=1; word_read <= limit; word_read++))
do
    if [ $word_read -eq $limit ] ; then
        { time head -n $word_read $train | cut -f 1 | python correction.py $voc "--$1" > "$1.txt" ; } \
            2>> $output_time
    else
        { time head -n $word_read $train | cut -f 1 | python correction.py $voc "--$1" > /dev/null ; } \
            2>> $output_time
    fi
done