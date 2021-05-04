
def site_absent(name):
    '''
    Ensure OMD site is NOT present 

    name
        OMD site to remove
    '''
    ret = {
        'name': name,
        'result': True,
        'comment' : '',
    }

    actions = []
    changes = {}

    if __opts__['test']:
        result = None
        dry_run = True
    else:
        result = True
        dry_run = False

    if __salt__['omd.site_exists'](name):
        if not dry_run:
            __salt__['omd.remove_site'](name)

        action = f"Site {name} removed"
        comment = action
        changes = { 'diff' : {
                'actions' : action,
                }
            }
    else:
        comment = f"Site {name} is already absent"
    

    ret.update({
        'result': result,
        'changes': changes,
        'comment' : comment,
    })

    return ret


def site_present(name, version=None, admin_password=None, no_tmpfs=None, tmpfs_size=None, params={}):
    '''
    Ensure OMD site is present with the specified parameters

    name
        OMD site to manage

    version
        OMD Version of the Site

    admin_password
        Set initial admin password

    tmpfs_size
        Size of the tmpfs volume 

    params
        Dictionary containing OMD configuration parameters
    '''

    ret = {
        'name': name,
        'result': True,
        'changes': {},
        'comment' : '',
    }

    actions = []

    if __opts__['test']:
        result = None
        dry_run = True
    else:
        result = True
        dry_run = False

    # Check omd site already exists
    if __salt__['omd.site_exists'](name):
        comment = f"OMD site {name} already exists"

        # Site exits!
        # Check site has the defined version
        old_version = __salt__['omd.site_version'](name)
        if old_version != version:
            # Version doesn't match specified version
            if not dry_run:
                __salt__['omd.update_site'](name,version)
            comment += f" but not with the defined version: {version}"
            actions.append(f"Update site from {old_version} -> {version}")
        else:
            # Version OK
            comment += f" with defined version: {version}"

    else:
        # Create new Site
        comment = f"Create new OMD site {name}"
        actions.append("Create new Site")        
        if not dry_run:
            __salt__['omd.create_site'](name, version, admin_password, no_tmpfs, tmpfs_size)


    # Check OMD Sites has the correct config params
    change_params = { 'old' : {}, 'new' : {} }

    # Compare current OMD Site config values with defined params  
    for key, val in params.items():
         if not __salt__['omd.site_is_config_value'](name, key, val):
            change_params['old'][key] = __salt__['omd.config_show_value'](name, key)
            change_params['new'][key] = val

    # If there changes in pipeline (change_params)
    if len(change_params['new']) > 0:
        actions.append("Modify Site configuration")
        if not dry_run:
            __salt__['omd.site_stop'](name)
            for key, val in change_params['new'].items():
                __salt__['omd.site_set_config_value'](name, key, val)
            __salt__['omd.site_start'](name)

    # If at least one action applied, report changes
    if len(actions) > 0:
        changes = { 'diff' : { 'actions' : actions } }
        # Extend dict if detailed changes are detected
        if len(change_params['new']) > 0:
            changes['diff']['detailed-changes'] = change_params
    else:
        comment += f" and specified parameters"
        changes = {}

    ret.update({
        'result': result,
        'changes': changes,
        'comment' : comment,
    })

    return ret
