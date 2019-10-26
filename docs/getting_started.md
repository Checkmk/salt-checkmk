# Getting Started
## Prerequisites  
- Running Salt environment 
- Formula is added to your Salt environment [Salt docs formulas](https://docs.saltstack.com/en/latest/topics/development/conventions/formulas.html#adding-a-formula-as-a-gitfs-remote)

**Example to include Formula:**
```bash
mkdir -p /srv/formulas
cd /srv/formulas
git clone https://github.com/tribe29/salt-checkmk
```

```bash
cp /srv/formulas/salt-checkmk/files/salt-checkmk.conf /etc/salt/master.d/
systemctl restart salt-master.service
```

Please consider recommendations from SaltStack:
>We strongly recommend forking a formula repository 



## Components and Setup

| Component        | Description                    | 
|------------------|------------------------------- |
|Salt Master       |Master of all Minions           |
|check**mk** Master|Monitoring Master pulls monitoring data from check**mk** Agents| 
|MK Minion         |The Minion which hosts the check**mk** installation (container, installed package, e.g.)
|Minions           |All Minions connected to the Salt Master -> including the MK Minion|


![setup](/docs/images/setup.png)



## Connect Salt with check**mk**
1. Log into your check**mk** environment

    In case that you have not already a running check**mk** Master, setup a new one e.g.:   
    https://hub.docker.com/r/checkmk/check-mk-raw
    
    ```bash
    docker container run -dit -p 8080:5000 -v /omd/sites --name monitoring -v /etc/localtime:/etc/localtime --restart always checkmk/check-mk-raw:1.6.0-latest
    
    #gather the logon credentials from container logs
    docker logs -f <id>
    ```
    Open your Browser and perform login to cmk container
    
     `http://localhost:8080/cmk`
    
    ![checkmk logon](/docs/images/cmk-logon.png)
    
    Click on the left sidebar on **WATO · Configuration** ->  "Users"
    
    Edit user `automation`:
    
    ![checkmk automation user](/docs/images/cmk-automation-user.png)
    
    Copy "Automation secret for machine accounts" (e.g. 7ffb0ff9-d907-4140-b95e-fb9d9df2a5)
    
2. Test the Salt check-mk-web-api Module
    
    ```bash
    salt-call saltutil.sync_all

    salt-call check-mk-web-api.call method=get_all_users target=localhost site=cmk port=8080 user=automation secret=<paste here the automation secret>
    ```

---
|**Previous**||||||**Next**|
|:-|-|-|------------|-|-|-:|
| < [Readme](../README.md) |||^[Top](#getting-started)||| [Pillar & Grains](cmk_pillar_grains.md)>| 