#!/bin/bash

STRUCTURE=$1
IND_MATERIALS=$2
FIDELITY=$3

NUM_CHUNKS=1000

for IND_CHUNK in $(seq 0 1 $[$NUM_CHUNKS - 1])
do
    echo $STRUCTURE $IND_MATERIALS $FIDELITY $NUM_CHUNKS $IND_CHUNK

    python ../src/run_simulation_chunk.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --num_chunks $NUM_CHUNKS --ind_chunk $IND_CHUNK
    sleep 0.1s
done
