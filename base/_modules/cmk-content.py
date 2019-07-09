'''
:maintainer: Philipp Lemke
:maturity: 201900
:requires: 
:platform: tested on Linux
'''
from __future__ import absolute_import
import logging
import salt.key
import salt.client
import pprint
import yaml

LOG = logging.getLogger(__name__)

def prepare(pillar_file, target, tgt_type=u'pillar', **kwargs):
    '''
    Gather grain information from salt minions to provide them as pillar data for the monitoring master.
    In "simple" Salt Setups, that can be done by using the Salt Mine. If you have a Master-of-Masters Setup this module can do the job for you, executed at the master-of-masters.  

    Params:
    pillar_file
    target
    tgt_type

    Example: salt-call cmk-content.prepare pillar_file=/srv/pillar/grains_for_monitoring.sls target="dbnode*" tgt_type=glob
    '''
    local = salt.client.LocalClient()
    try:
        #ret = local.cmd('mk-agent:True', 'grains.items', [], tgt_type)
        ret = local.cmd(target, 'grains.items', [], tgt_type)
        pillar = {'mk-host-grains' : ret }
        # Todo: Iter dict and write only valid returns in pillar
        # Handle this case ->
        # somehost: false
        with open(pillar_file, 'w') as output_stream:
            yaml.dump(pillar, output_stream, default_flow_style=False)
        return True
    except Exception as e:
        LOG.debug(pprint.pformat(e))

