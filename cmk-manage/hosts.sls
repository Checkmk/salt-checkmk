# -*- coding: utf-8 -*-
{% set site = pillar['cmk-master']['site'] %}
{% set user = pillar['cmk-master']['automation-user'] %}
{% set secret = pillar['cmk-master']['automation-secret'] %}
{% set port = pillar['cmk-master']['port'] %}
{% set graintags = pillar['cmk-master']['graintags'] %}


{% for host, data in pillar['mk-host-grains'].items() %}

ensure-host-in-wato-{{ host }}:
  cmk-manage.host_present:
    - name : {{ host}}
    - target : localhost
    - cmk_site : {{ site }}
    - cmk_user : {{ user }}
    - cmk_secret : {{ secret }}
    - port : {{ port }}
    - discover: False
    - ipaddress : {{ data['ipv4'][0] }}
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
