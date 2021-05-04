'''
Open Monitoring Distribution (OMD) Management Module

:maintainer: Philipp Lemke

:maturity: new

:depends: omd / checkmk

'''

import salt.exceptions
import subprocess
import logging
import os
from salt.exceptions import SaltException


def _check_site_config_value_exists(name, key):
    # This config keys won't be listed by omd config show
    # e.g. LIVESTATUS_TCP_PORT will be only displayed if LIVESTATUS_TCP is set
    # To prohibit errors the following list of keys will be ignored

    NO_CHECK_CONFIG_VALUES = ['LIVESTATUS_TCP_PORT', 'LIVESTATUS_TCP_TLS']

    if not (key in NO_CHECK_CONFIG_VALUES or site_config_value_exists(name, key)):
        raise salt.exceptions.CommandExecutionError("Config value [{}] does not exist.".format(key))

def _exec_nofetch(args):
     
    if isinstance(args, str):
        args = args.split()
    try:
        subprocess.check_call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        raise salt.exceptions.CommandExecutionError(str(e))

def _exec_fetch(args, ignore_errors=False):
    if isinstance(args, str):
        args = args.split()
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, err = p.communicate()
    if not ignore_errors:
        retcode = p.poll()
        if retcode:
            raise salt.exceptions.CommandExecutionError("Command '{cmd}' returned: {ret}".format(cmd=" ".join(args),ret=retcode))
    return output.decode('utf-8')


def omd_bool_encode(value):
    '''
    Encode defined omd config strings from boolean python values
    '''

    if isinstance(value, bool):
        if value :
            return "on"
        else:
            return "off"
    elif isinstance(value, str):
        return value
    elif isinstance(value, int):
        return str(value)
    else:
        raise salt.exceptions.CommandExecutionError("Unspecified value type. Value: {} must be a string or integer".format(value))

def omd_bool_decode(value):
    '''
    Decode defined omd strings to boolean python values
    '''

    if isinstance(value, str):
        if value.lower() == "on":
            return True
        elif value.lower() == "off":
            return False
        else:
            return value
    else:
        raise salt.exceptions.CommandExecutionError("Unsupported value type. Value: {} must be a string".format(value))


def _check_site_exists(name):
    if not site_exists(name):
        raise salt.exceptions.CommandExecutionError("Site [{}] does not exist.".format(name))

def sites():
    
    '''
    Show list of configured OMD sites
    '''
    # Show a list of all sites and the version of OMD each site uses.
    # Option  -b or --bare, prints output without a headline
    return _exec_fetch(['/usr/bin/omd', 'sites', '--bare']).splitlines()

def site_exists(name):
    
    '''
    Check OMD site still exists
    '''
    return name in sites()

def site_config_value_exists(name, key):
    '''
    Check OMD config value already exists
    '''
    return key in config_show(name)


def site_version(name):
    '''
    Return the version of the specified OMD site
    '''

    _check_site_exists(name)
    output = _exec_fetch(['/usr/bin/omd', 'version', name])
    return output.split()[-1]

def def_version():
    '''
    Return the currently set default version of OMD
    '''

    output = _exec_fetch(['/usr/bin/omd', 'version'])
    return output.split()[-1]

def versions():
    '''
    Return installed OMD versions
    '''

    versions = []
    output = _exec_fetch(['/usr/bin/omd', 'versions'])
    # 1.5.0p16.cre 
    # 1.6.0p8.cre (default)
    for line in output.splitlines():
        # honor only the first column
        versions.append(line.split()[0])
    return versions

def update_site(name, version=None, conflict='install'):
    '''
    Update SITE to the current default version of OMD or to the defined explicit defined VERSION
    '''

    # if site not exits, abort update
    _check_site_exists(name)

    site_stop(name)
    args = ['/usr/bin/omd', '--force']

    if version:
        target_version = version
        args.extend(['-V', version])
    else:
        #default version
        target_version = def_version()  
    
    if site_version(name) == target_version:
        return 'Site {} already at the defined version {}'.format(name,target_version)

    args.extend(['update', '--conflict', conflict])
    args.append(name)

    site_stop(name)
    logging.debug(args)
    output = _exec_fetch(args)
    site_start(name)
    return output

def create_site(name, version=None, admin_password=None, no_tmpfs=None, tmpfs_size=None):
    '''
    Create a new site. The name of the site must be at most 16 characters long and consist only of letters, digits and underscores. It cannnot begin with a digit.
    '''

    if site_exists(name):
        raise salt.exceptions.CommandExecutionError("Site [{}] already exists".format(name))

    args = ['/usr/bin/omd']
    
    if version:
        args.extend(['-V', version])

    args.append('create')

    if admin_password:
        args.extend(['--admin-password', admin_password])
    if no_tmpfs:
        args.append('--no-tmpfs')
    else:
        if tmpfs_size:
            args.extend(['-t', tmpfs_size])

    args.append(name)
    logging.debug(args)
    return _exec_fetch(args)

def remove_site(name):
    '''
    Remove existing OMD site (and its data)
    '''

    if not site_exists(name):
        raise salt.exceptions.CommandExecutionError("Site [{}] does not exist.".format(name))

    args = ['/usr/bin/omd', 'rm', name]
    p = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.STDOUT)
    output, err = p.communicate(input=b'yes\n')
    retcode = p.returncode

    if not retcode == 0 or err:
        raise salt.exceptions.CommandExecutionError("Command '{cmd}' Output: {output} Error: {err} Retcode: {ret}".format(cmd=" ".join(args), output=output, err=err, ret=retcode))
    else:
        return "Site [{}] successfully removed".format(name)

def site_status(name):
    
    '''
    Return component and overall status of the specified omd site
    '''

    _check_site_exists(name)
    ret = {}
    output = _exec_fetch(['/usr/bin/omd', 'status', '--bare', name], ignore_errors=True)
    for line in output.splitlines():
        key, value = line.split()
        ret[key] = int(value)
    return ret

def site_stopped(name):
    _check_site_exists(name)
    return site_status(name)['OVERALL'] == 1

def site_running(name):
    _check_site_exists(name)
    return site_status(name)['OVERALL'] == 0

def site_start(name):
    '''
    Start OMD site
    '''

    _exec_nofetch(['/usr/bin/omd', 'start', name])

def site_stop(name):
    '''
    Stop OMD site
    '''
    
    _exec_nofetch(['/usr/bin/omd', 'stop', name])
    return 'Site {} successfully stopped'.format(name)

def config_show(name):
    '''
    omd.config_show [SITE]
    Return the current settings of all variables of the specified SITE
    '''

    _check_site_exists(name)
    ret = {}
    output = _exec_fetch(['/usr/bin/omd', 'config', name, 'show'])
    for line in output.splitlines():
        k, v = line.split(': ')
        ret[k] = omd_bool_decode(v.strip())
    return ret

def config_show_value(name, key):
    '''
    omd.config_show [SITE] [VALUE]
    Return specific configuration value of an OMD Site
    '''
    args = ['/usr/bin/omd', 'config', name, 'show', key]
    _check_site_exists(name)
    _check_site_config_value_exists(name, key)

    ret = omd_bool_decode(_exec_fetch(args).strip())
    return ret

def site_is_config_value(name, key, value):
    '''
    Check configuration value of OMD site
    '''
    # Compare given config value with site config value
    return omd_bool_encode(config_show_value(name, key)) == omd_bool_encode(value)

def site_set_config_value(name, key, value):
    '''
    Set configuration value of OMD site
    '''
    args = ['/usr/bin/omd', 'config', name, 'set', key, omd_bool_encode(value)]
    _check_site_exists(name)
    _check_site_config_value_exists(name, key)
    if not site_stopped(name):
        raise salt.exceptions.CommandExecutionError("Site [{}] is currently running. Stop site before setting config values".format(name))

    ret = _exec_fetch(args)
    return ret


