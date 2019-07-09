from __future__ import absolute_import
import salt.exceptions
import logging
import salt.key
import salt.client
import re
import pprint

LOG = logging.getLogger(__name__)

global replace_chars
replace_chars = [(' ', '_'),
                 (',', '_'),
                 ('.', '-')]

def _convert_tag_list_to_dict(tag_list):
    tags = {}
    for tag in tag_list:
        tags.update({tag['id'] : tag })
    return tags

def _convert_tag_dict_to_tag_list(tag_dict):
    tags = []
    for k, v in tag_dict.items():
        tags.append(v)
    return tags

def _escape_tags(tag_dict):
    """
    Replace invalid tag charachters for mk conformity"

    Params:
    tag_dict: { 'tag_agent' : 'all-agents',
                'address_family' : 'ip-v4-only',
                'tag_db-khv' : 'db-khv',
              }
    """
    for k in tag_dict:
        for c1 ,c2 in replace_chars:
            tag_dict[k] = tag_dict[k].replace(c1,c2)

    return tag_dict


def _ensure_tag_ids_uniqueness(tag_dict_list):
    temp = {}
    for tag in tag_dict_list:
        temp[tag['id']] = tag

    tags_uniq = []    
    for k, v in temp.items():
        v['id'] = v['id'].replace(' ','_').replace('.','-').replace(',','_')
        tags_uniq.append(v)
    return tags_uniq



def _deploy_plugin(plugin, source):
    '''
    Use file.manage to deploy plugin
    '''
    return __states__['file.managed'](name=plugin, source=source)

def _ps_check(pattern):
    '''
    Check for running process and return True or False
    '''
    ret = False
    if __grains__['os'] == "Windows":
        if not __salt__['ps.pgrep'](pattern) == None:
            ret = True
    else:
        if len(__salt__['ps.psaux'](pattern)[1]) > 0:
            ret = True
    return ret


def dynamic_plugin_rollout(name, rulepack, source, instpath='DEFAULT'):
    '''
    Rollout Checkmk Agent Plugins based on:
    - by_installed_package
    - by_running_process
    - by_fs_object
    '''
    ret = {
        'name' : name,
        'changes': {},
        'result': True,
        'comment': [],
        'pchanges': {},
        }

    if instpath == 'DEFAULT':
        if __grains__['os'] == "Windows":
            instpath =  __salt__['environ.get']('ProgramFiles(x86)').replace("\\", "/") + '/check_mk/plugins'
        else:
            instpath = '/usr/lib/check_mk_agent/plugins'


    for plugin, rdata in rulepack.items():
        pluginpath = instpath + "/" + plugin
        sourcepath = source + "/" + plugin

        for pattern in rdata['match_patterns']:
            deploy = False
            #if re.match(r"%s" %pattern,   )
            if name == 'by_installed_package':
                if pattern in __salt__['pkg.list_pkgs']():
                    deploy = True

            elif name == 'by_running_process':
                if _ps_check(pattern):
                    deploy = True

            elif name == 'by_fs_object':
                if __salt__['file.file_exists'](pattern):
                    deploy = True

            if deploy:
                ret_deploy = _deploy_plugin(pluginpath, sourcepath)
                if not ret_deploy['result']:
                    ret['result'] = False
                ret['comment'].append(ret_deploy['comment'])
                ret['changes'].update(ret_deploy['changes'])
                #There is no need to deploy a plugin twice, so break loop here
                break
            
    if len(ret['comment']) == 0:
        ret['comment'] = 'No definition matched'

    return ret

def folder_present(name, target, cmk_site, cmk_user, cmk_secret, **custom_attrs):
    '''
    Ensure that the specified folder is present at the cmk target system

    Params: 
        name (string) = folder to add
    
    Example:
        name = '/customer1/datacenter2'

    '''
    ret = {
        'name' : name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
        }
    kwargs = {}

    base_kwargs = {  'method' : 'get_folder',
                'target' : target,
                'cmk_site' : cmk_site,
                'cmk_user' : cmk_user,
                'cmk_secret' : cmk_secret,
                 }
    #LOG.debug(pprint.pformat(custom_attrs))
    base_kwargs['folder'] = name

    kwargs.update(base_kwargs)
    #kwargs.update(custom_attrs)

    # add_folder expects another format for tag definitions
    if 'tags' in custom_attrs:
        for k,v in custom_attrs['tags'].items():
            k = 'tag_' + k
            custom_attrs.update({ k : v})
        custom_attrs.pop('tags')

    kwargs.update(custom_attrs)
    #LOG.debug(pprint.pformat(existing_folder))

    try: 
        api_ret = __salt__['check-mk-web-api.call'](**base_kwargs)
        LOG.debug(pprint.pformat(api_ret))
        new_properties = []
        for k, v in custom_attrs.items():
            if k not in api_ret['attributes']:
                # property currently not defined
                new_properties.append({ k : v})
            elif not v == api_ret['attributes'][k]:
                # property defined but value does not match salt definiton
                new_properties.append({ k : v})

        # merge definitions not managed by salt, to keep them
        #for k, v in api_ret['attributes'].items:
        #    if k not in new_properties:
        #        kwargs.update({api_ret['attributes'][k])

        LOG.debug("current attributes:")
        LOG.debug(pprint.pformat(api_ret['attributes']))


        LOG.debug("PROPERTY CHANGES:")
        LOG.debug(pprint.pformat(new_properties))
        if len(new_properties) > 0:
            ret['comment'] = "Folder exists but properties not matching with salt definitions"
            kwargs['method'] = 'edit_folder'
            api_ret = __salt__['check-mk-web-api.call'](**kwargs)
            ret['changes'] = {'Properties changed:' : new_properties }
            ret['result'] = True
        else:
            ret['comment'] = "Folder '%s' already exists and has the right properties" %name
            ret['result'] = True

    except Exception as e:
        if re.match(r'Check_MK exception: Folder .* does not exist', str(e)) is not None:
            ret['result'] = True
            kwargs['method'] = 'add_folder'
            api_ret = __salt__['check-mk-web-api.call'](**kwargs)
            ret['changes'] = {'Folder added' : name}
            ret['comment'] = "Add Folder %s" %name
        else:
            ret['comment'] = pprint.pformat(e)
 
    return ret

def folder_absent(name, target, cmk_site, cmk_user, cmk_secret):
    '''
    Ensure that the specified folder is absent at the cmk target system

    Params: 
        name (string) = folder to delete
    
    Example:
        name = '/customer1/datacenter2'

    Remark: Subfolders will be also deleted
    '''
    ret = {
        'name' : name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
        }
    kwargs = {}

    base_kwargs = {  'method' : 'get_all_folders',
                'target' : target,
                'cmk_site' : cmk_site,
                'cmk_user' : cmk_user,
                'cmk_secret' : cmk_secret,
                 }
    
    kwargs.update(base_kwargs)
    kwargs['method'] = 'delete_folder'

    existing_folders = __salt__['check-mk-web-api.call'](**base_kwargs)
    api_ret = False

    for folder in existing_folders:
        if name == folder:
            kwargs['folder'] = name
            api_ret = __salt__['check-mk-web-api.call'](**kwargs)

    if api_ret == None:
        ret['result'] = True
        ret['changes'] = {'Folder deleted' : name}
    elif not api_ret:
        ret['result'] = True
        comment = 'Folder already absent'
    else:
        comment = 'Exception: %s' %api_ret

    ret['comment'] = comment
    return ret

def host_present(name, target, cmk_site, cmk_user, cmk_secret, discover=False, **custom_attrs):
    '''
    Ensure that the specified host is present at the cmk target system
    TODO:  and has the defined attributes
    '''
    ret = {
        'name' : name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
        }

    LOG.debug(pprint.pformat(custom_attrs))
    kwargs = {}
    base_kwargs = {  'method' : 'add_host',
                'target' : target,
                'cmk_site' : cmk_site,
                'cmk_user' : cmk_user,
                'cmk_secret' : cmk_secret,
                'hostname' : name
                 }
    
    kwargs.update(base_kwargs)
    kwargs.update(custom_attrs)

    if 'tags' in kwargs:
        #LOG.error(kwargs['tags')
        kwargs['tags'] = _escape_tags(kwargs['tags']) 

    try: 
        api_ret = __salt__['check-mk-web-api.call'](**kwargs)
        #if api_ret == None:
        if discover:
            base_kwargs['method'] = 'discover_services'
            __salt__['check-mk-web-api.call'](**base_kwargs)

        ret['result'] = True
        ret['changes'] = {  'Host added' : { 'Hostname' : name,
                                             'Params' : custom_attrs, }
                         }
    except Exception as e:
        if re.match(r'Check_MK exception: Host .* already exists in the folder', str(e)) is not None:
            ret['result'] = True
            ret['comment'] = "Host already exists"
        else:
            ret['comment'] = pprint.pformat(e)

    return ret


def hosttags_present(name, target, cmk_site, cmk_user, cmk_secret, aux_tags={}, tag_groups={}):
    '''
    Ensure that the specified hosttags are present at the cmk target system

    Example params:
    ---------------
    aux_tags = { 'rp' : {'id': 'rp', 'title': 'Rheinland-Pfalz'},
                 'by' : {'id': 'by', 'title': 'Bayern'},
                }

    tag_groups = { 'city' : { 'id' : 'city',
                    'title' : 'City where the system is located',
                    'topic' : 'Location Tags',
                    'tags': [ {'aux_tags': ['rp'], 'id': 'trier', 'title': 'Trier'},
                              {'aux_tags': ['by'], 'id': 'muenchen','title': 'Muenchen'},
                              {'aux_tags': ['be'], 'id': 'berlin','title': 'Berlin'},
                            ],
                  },
                }

    '''
    ret = {
        'name' : name,
        'changes': {},
        'result': False,
        'comment': '',
        'pchanges': {},
        }

    changes = {'Auxilary Tags added' : [], 'Auxilary Tags updated' : [], 'Tag groups added' : [], 'Tag groups updated' : [] }

    
    for tag_group in tag_groups:
        tag_groups[tag_group]['tags'] = _ensure_tag_ids_uniqueness(tag_groups[tag_group]['tags'])


    #LOG.debug(pprint.pformat(custom_attrs))
    kwargs = {  'method' : 'get_hosttags',
                'target' : target,
                'cmk_site' : cmk_site,
                'cmk_user' : cmk_user,
                'cmk_secret' : cmk_secret,
                 }
    LOG.debug("aux_tags_params(%s): %s" %(type(aux_tags), aux_tags))
    LOG.debug("tag_groups params(%s): %s" %(type(tag_groups), tag_groups))
    
    #get current host tags 
    current_hosttags = __salt__['check-mk-web-api.call'](**kwargs)
    

    current_hosttags["aux_tags"] = _convert_tag_list_to_dict(current_hosttags['aux_tags'])
    for key, data_dict in aux_tags.items():
        if key in current_hosttags['aux_tags']:
            # existing tag found, 
            if not data_dict == current_hosttags['aux_tags'][key]:
                # update taggroup with new content
                current_hosttags['aux_tags'][key] = data_dict
                changes['Auxilary Tags updated'].append(key)
            else:
                #nothing to do 
                pass

        else:
            current_hosttags['aux_tags'][key] = data_dict
            changes['Auxilary Tags added'].append(key)
    current_hosttags['aux_tags'] = _convert_tag_dict_to_tag_list(current_hosttags['aux_tags'])


    current_hosttags['tag_groups'] = _convert_tag_list_to_dict(current_hosttags['tag_groups'])
    for key, data_dict in tag_groups.items():
        if key in current_hosttags['tag_groups']:
            # existing tag found, 
            if not data_dict == current_hosttags['tag_groups'][key]:
                # update taggroup with new content
                current_hosttags['tag_groups'][key] = data_dict
                changes['Tag groups updated'].append(key)
            else:
                #nothing to do 
                pass

        else:
            current_hosttags['tag_groups'][key] = data_dict
            changes['Tag groups added'].append(key)
    current_hosttags['tag_groups'] = _convert_tag_dict_to_tag_list(current_hosttags['tag_groups'])

    ret['comment'] = pprint.pformat(current_hosttags['tag_groups'])

    kwargs['method'] = 'set_hosttags'
    kwargs['hosttags'] = current_hosttags
    api_ret = __salt__['check-mk-web-api.call'](**kwargs)

    num_changes = 0
    for k,v in changes.items():
        num_changes += len(v)

    if num_changes > 0:
        ret['changes'] = changes
        ret['comment'] = '%s Tag definitions updated' %num_changes

        kwargs['method'] = 'activate_changes'
        kwargs['allow_foreign_changes'] = True
        kwargs.pop('hosttags')
        __salt__['check-mk-web-api.call'](**kwargs)

    else:
        ret['comment'] = 'Tags are already in the correct state'

    if api_ret == None:
            ret['result'] = True

    return ret