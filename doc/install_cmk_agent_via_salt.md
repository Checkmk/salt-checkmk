# Install check*mk* Agent via Salt

## Prerequisites  
- CMK Site is already running
- Linux msitools installed
--- 

1. Ensure check*mk* Agents are available in Salt file_root


    ```bash
    docker ps
    ```

    ```bash
    cd /srv/salt/blobs/check_mk/agents/windows

    docker cp <containerId>:/opt/omd/versions/1.6.0p3.cre/share/check_mk/agents/windows .

    AGENTVERSION=$(msiinfo export check_mk_agent.msi Property|grep ProductVersion|awk '{print $2}'|tr -d '\r\n')

    mv check_mk_agent.msi check_mk_agent_${AGENTVERSION}.msi 
    ```


## Installation unter Windows

**Definition der Paketversionen**

Anlegen des "[winrepo_source_dir-Verzeichnisses](https://docs.saltstack.com/en/latest/ref/configuration/minion.html#winrepo-source-dir)":
```bash
mkdir -p /srv/salt/win/repo-ng/salt-winrepo-ng
```

Bekanntmachen der Agenten-Versionen im Salt Package Management

```bash
vim /srv/salt/win/repo-ng/salt-winrepo-ng/check-mk-agent-msi.sls
```

Inhalt:
```
check-mk-agent:
  '1.5.0.3264':
    full_name: 'Check_MK Agent'
    installer: 'salt://blobs/check_mk/1.5.0p2/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.5.0p2/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False

  '1.5.0.3266':
    full_name: 'Check_MK Agent'
    installer: 'salt://blobs/check_mk/1.5.0p9.cre/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.5.0p9.cre/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False

  '1.5.0.3268':
    full_name: 'Check_MK Agent'
    installer: 'salt://blobs/check_mk/1.5.0p11.cee/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.5.0p11.cee/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False

```

Mit folgendem Befehl werden die package definition files (.sls) im [winrepo_source_dir-Verzeichnis](https://docs.saltstack.com/en/latest/ref/configuration/minion.html#winrepo-source-dir) (default salt://win/repo-ng) auf den Windows-Minion übertragen und lokal gecached (default: `C:\salt\var\cache\salt\minion\files\base\winrepo-ng\`)

```bash
# salt -G 'os:windows' pkg.refresh_db
mkwin10:
    ----------
    failed:
        0
    success:
        1
    total:
        1

```

**Installation auf dem Minion** 

Die Funktion `pgk.install` installiert die MSI-Version `1.5.0.3264` des eben definierten Packages `check-mk-agent` auf dem System `mkwin10`:

```bash
# salt mkwin10 pkg.install check-mk-agent version=1.5.0.3264
mkwin10:
    ----------
    check-mk-agent:
        ----------
        new:
            1.5.0.3264
        old:
```

**Update auf eine höhere Version**

```bash
# salt mkwin10 pkg.install check-mk-agent version=1.5.0.3266
```
Ergebnis:
```
mkwin10:
    ----------
    check-mk-agent:
        ----------
        new:
            1.5.0.3266
        old:
            1.5.0.3264

```

**Salt States** 

Die Test-Installation des Agenten erfolgte über ein sogenantes Salt Execution Module. Um eine bessere Abstraktion zu ermöglichen, empfiehlt sich aber die Definition eines "States" für die Installation des Agenten.

Sobald dieser State auf ein System angewendet wird, versucht Salt das Zielsystem in den Zustand zu versetzen, welcher im State beschrieben ist.
 
Anlegen eines Salt State Files (sls):

```bash
# vim /srv/salt/deploy/check-mk-agent.sls
check-mk-agent:
  pkg.installed:
    - version : 1.5.0.3268
```

Installation/Update des Agenten via "state.apply":

```bash
# salt mkwin10 state.apply deploy.check-mk-agent
```

Da im State die Zielversion "1.5.0.3268" definiert ist, führt Salt ein Update des Check_MK Agenten durch:
```
mkwin10:
----------
          ID: check-mk-agent
    Function: pkg.installed
      Result: True
     Comment: 1 targeted package was installed/updated.
     Started: 22:25:31.053000
    Duration: 3859.0 ms
     Changes:   
              ----------
              check-mk-agent:
                  ----------
                  new:
                      1.5.0.3268
                  old:
                      1.5.0.3266

Summary for mkwin10
------------
Succeeded: 1 (changed=1)
Failed:    0
------------
Total states run:     1
Total run time:   3.859 s
```
Eine weitere Anwendung des States führt zu folgenden Ergebnis:

```bash
# salt mkwin10 state.apply deploy.check-mk-agent
mkwin10:
----------
          ID: check-mk-agent
    Function: pkg.installed
      Result: True
     Comment: All specified packages are already installed and are at the desired version
     Started: 22:26:12.130000
    Duration: 2437.0 ms
     Changes:   

Summary for mkwin10
------------
Succeeded: 1
Failed:    0
------------
Total states run:     1
Total run time:   2.437 s

```
**Quellen**
* [Salt Windows Software Repository](https://docs.saltstack.com/en/latest/topics/windows/windows-package-manager.html)




## Installation unter Linux
Anlegen / Updaten des Salt State Files (sls):

```
vim /srv/salt/deploy/check-mk-agent.sls
```
Inhalt:
```
{% if grains['os_family'] == 'Windows' %}
check-mk-agent-win:
  pkg.installed:
    - version : 1.5.0.3268

{% elif grains['os_family'] == 'Debian' %}
check-mk-agent:
  pkg.installed:
    - sources:
      - check-mk-agent: salt://blobs/check_mk/1.5.0p7.cee/share/check_mk/agents/check-mk-agent_1.5.0p7-1_all.deb
    - refresh: False

{% elif grains['os_family'] == 'RedHat' %}
check-mk-agent:
  pkg.installed:
    - sources:
      - check-mk-agent: salt://blobs/check_mk/1.5.0p7.cee/share/check_mk/agents/check-mk-agent-1.5.0p7-1.noarch.rpm
    - refresh: False

{% endif %}
```
Installation des Agenten via "state.apply"

```bash
salt linux-vm state.apply deploy.check-mk-agent
```
```
linux-vm:
----------
          ID: check-mk-agent
    Function: pkg.installed
      Result: True
     Comment: The following packages were installed/updated: check-mk-agent
     Started: 22:57:45.835309
    Duration: 4740.395 ms
     Changes:   
              ----------
              check-mk-agent:
                  ----------
                  new:
                      1.5.0p7-1
                  old:

Summary for linux-vm
------------
Succeeded: 1 (changed=1)
Failed:    0
------------
Total states run:     1
Total run time:   4.740 s
```
