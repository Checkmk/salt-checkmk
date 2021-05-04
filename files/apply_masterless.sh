#!/bin/bash
MINION_CONFD=/etc/salt/minion.d
FORMULA_PATH=/srv/formulas/salt-checkmk
PILLAR_PATH=/srv/pillar

# create default folders
mkdir -p /srv/salt $PILLAR_PATH

# copy minion conf & default pillar
cp $FORMULA_PATH/files/masterless.conf $MINION_CONFD
cp $FORMULA_PATH/files/pillar_top.sls $PILLAR_PATH/top.sls
cp $FORMULA_PATH/pillar.example $PILLAR_PATH/omd.sls

# sync execution modules and states
salt-call --local saltutil.sync_all
