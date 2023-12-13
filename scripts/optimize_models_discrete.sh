#!/bin/bash

ALGORITHMS='rs pybobyqa powell de direct bo'

##
STRUCTURE='threelayers2d'
IND_MATERIALS=0
FIDELITY='high'
PROPERTY='transmittance'

for ALGORITHM in $ALGORITHMS
do
    for IND_ROUND in $(seq 0 1 49)
    do
        echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY $ALGORITHM $IND_ROUND

        python ../src/optimize_algorithms.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY --algorithm $ALGORITHM --ind_round $IND_ROUND --discrete
        sleep 0.1s
    done
done

##
STRUCTURE='nanocones2d'
IND_MATERIALS=0
FIDELITY='high'
PROPERTY='reflectance'

for ALGORITHM in $ALGORITHMS
do
    for IND_ROUND in $(seq 0 1 49)
    do
        echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY $ALGORITHM $IND_ROUND

        python ../src/optimize_algorithms.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY --algorithm $ALGORITHM --ind_round $IND_ROUND --discrete
        sleep 0.1s
    done
done

##
STRUCTURE='nanospheres2d'
IND_MATERIALS=0
FIDELITY='high'
PROPERTY='absorbance'

for ALGORITHM in $ALGORITHMS
do
    for IND_ROUND in $(seq 0 1 49)
    do
        echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY $ALGORITHM $IND_ROUND

        python ../src/optimize_algorithms.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY --algorithm $ALGORITHM --ind_round $IND_ROUND --discrete
        sleep 0.1s
    done
done

##
STRUCTURE='nanowires2d'
IND_MATERIALS=0
FIDELITY='high'
PROPERTY='absorbance'

for ALGORITHM in $ALGORITHMS
do
    for IND_ROUND in $(seq 0 1 49)
    do
        echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY $ALGORITHM $IND_ROUND

        python ../src/optimize_algorithms.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY --algorithm $ALGORITHM --ind_round $IND_ROUND --discrete
        sleep 0.1s
    done
done

##
STRUCTURE='doublenanocones2d'
IND_MATERIALS=0
FIDELITY='high'
PROPERTY='transmittance'

for ALGORITHM in $ALGORITHMS
do
    for IND_ROUND in $(seq 0 1 49)
    do
        echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY $ALGORITHM $IND_ROUND

        python ../src/optimize_algorithms.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY --algorithm $ALGORITHM --ind_round $IND_ROUND --discrete
        sleep 0.1s
    done
done
