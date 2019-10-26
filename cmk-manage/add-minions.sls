{% set site = pillar['cmk-master']['site'] %}
{% set user = pillar['cmk-master']['automation-user'] %}
{% set secret = pillar['cmk-master']['automation-secret'] %}
{% set port = pillar['cmk-master']['port'] %}
{% set graintags = pillar['cmk-master']['graintags'] %}


# It is necessary to do this before you add your hosts to the monitoring system,
# because a Host-Tag must exist before you are able to assign them.

ensure-hosttags-present-in-wato:
  cmk-manage.hosttags_present:
    - name : hosttags_present
    - target : localhost
    - cmk_site : {{ site }}
    - cmk_user : {{ user }}
    - cmk_secret : {{ secret }}
    - port : {{ port }}
    - tag_groups:
        {% for graintag in graintags %}
          {{ graintag }}:
            id : {{ graintag }}
            title : {{ graintag }}
            topic : Salt Grains
            tags:
          {% for sold_to in pillar['mk-host-grains'] %}
            {% for host, data in pillar['mk-host-grains'].items() %}
              {% if graintag in data %}
              - id : "{{ graintag}}_{{ data[graintag] }}"
                title : "{{ data[graintag] }}"
                aux_tags: []
              {% endif %}
            {% endfor %}
          {% endfor %}
        {% endfor %}

{% for host, data in pillar['mk-host-grains'].items() %}
{% if 'cmk-agent-ip' in data %}
  {%set cmkagentip =  data['cmk-agent-ip'] %}
{% else %}
  {%set cmkagentip =  data['ipv4'][0] %}
{% endif %}

ensure-host-in-wato-{{ host }}:
  cmk-manage.host_present:
    - name : {{ host}}
    - target : localhost
    - cmk_site : {{ site }}
    - cmk_user : {{ user }}
    - cmk_secret : {{ secret }}
    - port : {{ port }}
    - discover: False
    - ipaddress : {{ cmkagentip }}
    - alias : {{ data['host'] }}
{#    - folder : {{ folder }} #}
    - tags: {
        {% for graintag in graintags %}
            {% if graintag in data %}
                {{ graintag }} : '{{ graintag }}_{{ data[graintag] }}',
            {% endif %}
        {% endfor %}
            } 
{% endfor %}