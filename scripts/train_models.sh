#!/bin/bash

FIDELITY='high'

##
STRUCTURE='threelayers2d'
IND_MATERIALS=0
PROPERTY='transmittance'

echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY

python ../src/train_mlp.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY
sleep 0.1s

##
STRUCTURE='nanocones2d'
IND_MATERIALS=0
PROPERTY='reflectance'

echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY

python ../src/train_mlp.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY
sleep 0.1s

##
STRUCTURE='nanospheres2d'
IND_MATERIALS=0
PROPERTY='absorbance'

echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY

python ../src/train_mlp.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY
sleep 0.1s

##
STRUCTURE='nanowires2d'
IND_MATERIALS=0
PROPERTY='absorbance'

echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY

python ../src/train_mlp.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY
sleep 0.1s

##
STRUCTURE='doublenanocones2d'
IND_MATERIALS=0
PROPERTY='transmittance'

echo $STRUCTURE $IND_MATERIALS $FIDELITY $PROPERTY

python ../src/train_mlp.py --structure $STRUCTURE --ind_materials $IND_MATERIALS --fidelity $FIDELITY --property $PROPERTY
sleep 0.1s
