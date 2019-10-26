check-mk-agent:
  '1.6.0p3':
    full_name: 'Check MK Agent 1.6'
    installer: 'salt://blobs/check_mk/1.6.0p3/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/1.6.0p3/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False
