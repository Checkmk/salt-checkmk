#!py
import copy

def run():
    state_config = {}
  
    for site, specific_config in __pillar__['omd']['sites'].items():
        config = copy.deepcopy(__pillar__['omd']['defaults'])
  
        if 'base' in specific_config:
            config['base'].update(specific_config['base'])
        if 'params' in specific_config:
            config['params'].update(specific_config['params'])
          
        base = config['base']
        
        state = 'omd.site_present'
        state_id = f'ensure-omd-site-{site}-present'

        state_config[state_id] =  { state : [
            { 'name' : site },
            { 'version' : base['version'] },
            { 'params' : config['params'] },
            ]
          }

        if  base['no_tmpfs']:
            state_config[state_id][state].append({ 'no_tmpfs' : True })
        elif base['tmpfs_size']:
            state_config[state_id][state].append({ 'tmpfs_size' : base['tmpfs_size'] })
  
    return state_config

