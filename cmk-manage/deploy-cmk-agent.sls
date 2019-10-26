{% set cmkversion='1.6.0p3' %}
{% if grains['os_family'] == 'Windows' %}
check-mk-agent:
  pkg.installed:
    - version : {{ cmkversion }}

{% elif grains['os_family'] == 'Debian' %}
check-mk-agent:
  pkg.installed:
    - sources:
      - check-mk-agent: salt://blobs/check_mk/{{ cmkversion }}/share/check_mk/agents/check-mk-agent_{{ cmkversion }}-1_all.deb
    - refresh: False

{% elif grains['os_family'] == 'RedHat' %}
check-mk-agent:
  pkg.installed:
    - sources:
      - check-mk-agent: salt://blobs/check_mk/{{ cmkversion }}/share/check_mk/agents/check-mk-agent-{{ cmkversion }}-1.noarch.rpm
    - refresh: False

{% endif %}
