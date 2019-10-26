# -*- coding: utf-8 -*-
{% set site = pillar['cmk-master']['site'] %}
{% set user = pillar['cmk-master']['automation-user'] %}
{% set secret = pillar['cmk-master']['automation-secret'] %}
{% set port = pillar['cmk-master']['port'] %}
{% set graintags = pillar['cmk-master']['graintags'] %}

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
          - id : "{{graintag}}_{{ data[graintag] }}"
            title : "{{ data[graintag] }}"
            aux_tags: []
          {% endif %}
        {% endfor %}
        {% endfor %}
        {% endfor %}


