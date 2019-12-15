{% for plugin, p_data in salt['pillar.get']('mk-plugin-mapping:by_installed_package', {}).iteritems() %}

    {% for pattern in p_data['match_patterns'] %}
        {% if pattern in  salt['pkg.list_pkgs']() %}

        deploy-mk-plugin-{{plugin}}-{{pattern}}:
            file.managed:

            {% if grains['os']  == 'Windows' %}
                {% set ProgramFiles = salt['environ.get']('ProgramFiles(x86)').replace("\\", "/") %}
                - name : "{{ProgramFiles}}/check_mk/plugins/{{plugin}}"
                - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/windows/plugins/{{plugin}}

            {% else %}
                - name : /usr/lib/check_mk_agent/plugins/{{plugin}}
                - source: salt://blobs/check_mk/{{pillar['mk-base']['version']}}/share/check_mk/agents/plugins/{{plugin}}
                - mode: 744
                - user: root
                - group: root

        set-autotag-grain-{{plugin}}-{{pattern}}:
            file.managed:
                - name: {{ salt['config.get']('conf_file') }}.d/autotags.conf
                - contents: |
                    grains:
                        salt_autotags :
                            application_tags : {{pattern}}

            {% endif %}
        {% endif %}
    {% endfor %}
{% endfor %}
