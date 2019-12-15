check-mk-agent-msi:
  {% for version in ['1.5.0p9', '1.4.0.2857', '1.4.0p15', '1.2.8.1521', '1.2.8p26', '1.2.8b4', '1.2.8b3', '1.2.8b2', '1.2.8b1', '1.2.7i3p5', '1.2.7i3p4', '1.2.7i3p3', '1.2.7i3p2', '1.2.7i3p1', '1.2.6.185', '1.2.6p16', '1.2.6p15', '1.2.6p14', '1.2.6p13', '1.2.6p12'] %}
  '{{ version }}':
    full_name: 'Check_MK Agent {{ version }}'
    installer: 'salt://blobs/check_mk/{{ version }}/share/check_mk/agents/windows/check_mk_agent.msi'
    install_flags: '/qn /norestart'
    uninstaller: 'salt://blobs/check_mk/{{ version }}/share/check_mk/agents/windows/check_mk_agent.msi'
    uninstall_flags: '/qn /norestart'
    msiexec: True
    locale: en_US
    reboot: False
  {% endfor %}
