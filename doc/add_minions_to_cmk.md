# Add Salt Minions to a check**mk** monitoring environment

## Prerequisites  
- CMK Site is already running
- Test of check-mk-web-api was successful

--- 

Now we have to provide the minion which communicates with our checkmk site the following data.

- Monitoring Site
- Automation User
- Automation Secret
- HTTP Port
- Graintags 


1. Store cmk access data in pillar e.g. /srv/pillar/cmk-base.sls

    ```yaml
    cmk-master:
      site: cmk
      automation-user: automation
      automation-secret: <paste here the automation secret>
      graintags: ['kernel', 'manufacturer', 'osfinger', 'virtual', 'productname']

    ```
    All Grains which are defined in graintags will be pushed later to the cmk monitoring site and can be reused there

2. Gather Grain data from all minions that you plan to add to the monitoring site

    ```bash
    salt-call cmk_content.prepare pillar_file=/srv/pillar/grains_for_monitoring.sls target="*" tgt_type=glob 
    ```


3. Assign Pillar to minion
    ```yaml
    base:
      '<your minion>':
        - cmk-base
        - grains_for_monitoring
    ```
    Test ->  `salt-call pillar.items`

    ![Output](/doc/images/pillar_items_cmk_master.png)


4. Add Host-Tags based on Grains to the monitoring site

    ```bash
    salt-call state.apply cmk-manage.hosttags
    ```

    It is necessary to do this before you add your hosts into the monitoring, because a Tag must exist before you are able to assign them.

    
5. Add your Minions as Monitoring-Hosts in the cmk monitoring site

    ```bash
    salt-call state.apply cmk-manage.hosts
    ```


