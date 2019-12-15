{% set source = 'salt://blobs/check_mk/' + pillar['mk-base']['version'] + '/share/check_mk/agents/plugins' %}

{% if grains['os']  == 'Windows' %}
    {% set source = 'salt://blobs/check_mk/' + pillar['mk-base']['version'] + '/share/check_mk/agents/windows/plugins' %}
{% endif %}

cmk-agent-plugins-by-installed-package:
  cmk-manage.dynamic_plugin_rollout:
    - name: by_installed_package
    - rulepack: {{ salt['pillar.get']('mk-plugin-mapping:by_installed_package', {}) }}
    - source: {{ source }}

cmk-agent-plugins-by-running-process:
  cmk-manage.dynamic_plugin_rollout:
    - name: by_running_process
    - rulepack: {{ salt['pillar.get']('mk-plugin-mapping:by_running_process', {}) }}
    - source: {{ source }}

cmk-agent-plugins-by-fs-object:
  cmk-manage.dynamic_plugin_rollout:
    - name: by_fs_object
    - rulepack: {{ salt['pillar.get']('mk-plugin-mapping:by_fs_object', {}) }}
    - source: {{ source }}

