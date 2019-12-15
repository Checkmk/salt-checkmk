{% for plugin, p_data in salt['pillar.get']('mk-plugin-mapping:by_fs_object', {}).iteritems() %}

    {% for pattern in p_data['match_patterns'] %}
        {% if salt['file.file_exists'](pattern) %}

        deploy-mk-plugin-{{plugin}}-{{pattern}}:
            file.managed:

            {% if grains['os']  == 'Windows' %}
                {% set ProgramFiles = salt['environ.get']("ProgramFiles(x86)").replace("\\", "/") %}
                - name : "{{ProgramFiles}}/check_mk/plugins/{{plugin}}"
                - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/windows/plugins/{{plugin}}

            {% else %}
                - name : /usr/lib/check_mk_agent/plugins/{{plugin}}
                - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/plugins/{{plugin}}
                - mode: 744
                - user: root
                - group: root

            {% endif %}
        {% endif %}
    {% endfor %}
{% endfor %}
