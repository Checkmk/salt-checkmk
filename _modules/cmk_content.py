'''
:maintainer: Philipp Lemke / Christian Dewald
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

def prepare(pillar_file, target, tgt_type=u'pillar', prefix=None, **kwargs):
    '''
    Gather grain information from salt minions to provide them as pillar data for the monitoring master.
    In "simple" Salt Setups, that can be done by using the Salt Mine. If you have a Master-of-Masters Setup this module can do the job for you, executed at the master-of-masters.  

    Args:
    pillar_file (str): Pillar file to store data
    target (str)  
    tgt_type (str)
    prefix (str): Prefix key within mk-host-grains pillar data. In some situations useful to merge data

    CLI Example:
    
        salt-call cmk_content.prepare pillar_file=/srv/pillar/grains_for_monitoring.sls target="dbnode*" tgt_type=glob prefix=syndic_x
    '''
    local = salt.client.LocalClient()

    ret = local.cmd(target, 'grains.items', [], tgt_type)
    graintags = {}

    # try to fetch graintags from pillars
    try:    
        grain_tag_list =  __pillar__['cmk-master']['graintags']
    except:
        grain_tag_list = False

    #if the minion did not answer, grains will be False, those hosts will be skipped
    for minion, grains in ret.items():
        if grains:
            graintags[minion] = {}
            if grain_tag_list:
                for grain in grain_tag_list:
                    graintags[minion][grain] = str(grains[grain])
            # Fallback gather all grains from minion
            else:
                graintags[minion] = grains


    if prefix:
        pillar = {'mk-host-grains' : { prefix : graintags }}
    else:
        pillar = {'mk-host-grains' : graintags }

    with open(pillar_file, 'w') as output_stream:
        yaml.dump(pillar, output_stream, default_flow_style=False)

    return "Grain data from %s hosts gathered" %len(ret)
    

