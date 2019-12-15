{% for plugin, p_data in salt['pillar.get']('mk-plugin-mapping:by_running_process', {}).iteritems() %}

    {% for pattern in p_data['match_patterns'] %}
        {% if grains['os']  == 'Windows' %}

            {% if not salt['ps.pgrep'](pattern) == None %}
                {% set ProgramFiles = salt['environ.get']("ProgramFiles(x86)").replace("\\", "/") %}

                deploy-mk-plugin-{{plugin}}-{{pattern}}:
                    file.managed:
                    - name : "{{ProgramFiles}}/check_mk/plugins/{{plugin}}"
                    - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/windows/plugins/{{plugin}}
            {% endif %}

        {% else %}
            {% if salt['ps.psaux'](pattern)[1]|length > 0  %}
                deploy-mk-plugin-{{plugin}}-{{pattern}}:
                    file.managed:
                        - name : /usr/lib/check_mk_agent/plugins/{{plugin}}
                        - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/plugins/{{plugin}}
                        - mode: 744
                        - user: root
                        - group: root
            {% endif %}

        {% endif %}
    {% endfor %}
{% endfor %}
