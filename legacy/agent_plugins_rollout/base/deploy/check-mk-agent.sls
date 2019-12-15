{% if grains['os_family'] == 'Windows' %}
check-mk-agent:
  pkg.installed:
    - version : 1.5.0.3268

{% elif grains['os_family'] == 'Debian' %}
check-mk-agent:
  pkg.installed:
    - sources:
      - check-mk-agent: salt://blobs/check_mk/1.5.0p7.cee/share/check_mk/agents/check-mk-agent_1.5.0p7-1_all.deb
    - refresh: False

{% endif %}
