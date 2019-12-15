check-mk-agent:
  '1.5.0.3264':
    full_name: 'Check_MK Agent'
    installer: 'salt://blobs/check_mk/1.5.0p2.cee/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.5.0p2.cee/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False

  '1.5.0.3266':
    full_name: 'Check_MK Agent'
    installer: 'salt://blobs/check_mk/1.5.0p9.cee/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.5.0p9.cee/share/check_mk/agents/windows/check_mk_agent.msi'
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

