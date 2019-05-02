# Combine check**mk** & Salt 

## Abstract
This project describes how you can combine the powerful solutions check**mk** (monitoring) & **Salt** (automation)

## Recommendations:
It would be useful if you have experience with one of the both solutions.

check**mk** perspective
> How to use Salt to improve or support your existing check**mk** monitoring environment

Salt perspective
>How to setup easily a whole monitoring environment to monitor your minions in-depth

---

The following Salt components will be provided for an easy integration:

### Salt Excecution Module
- check-mk-web-api

### Salt State Module
- cmk-manage

---
Topics:
- Install the check**mk** Agent via Salt
- Automatically add your Salt Minions to a check**mk** monitoring environment
- Dynamic Rollout of checkmk Agent Plugins
- Tag check**mk** Hosts based on Salt Grains


## Getting Started

1. Log into your check**mk** environment

In case that you have not already a running check**mk** environment, setup a new one e.g.:   
https://hub.docker.com/r/checkmk/check-mk-raw

```bash
docker container run -dit -p 8080:5000 -v /omd/sites --name monitoring -v /etc/localtime:/etc/localtime --restart always checkmk/check-mk-raw:1.5.0-latest

#gather the logon credentials from container logs
docker logs -f <id>
```

![checkmk logon](/doc/images/cmk-logon.png)

Click on the left sidebar on **WATO · Configuration** ->  "Users"

Edit user `automation`:

![checkmk automation user](/doc/images/cmk-automation-user.png)

Copy "Automation secret for machine accounts" (e.g. 7ffb0ff9-d907-4140-b95e-fb9d9df2a5)

2. Test the Salt check-mk-web-api Module

```bash
salt-call check-mk-web-api.call method=get_all_users target=localhost site=cmk port=8080 user=automation secret=<paste here the automation secret>
```

3. cmk-mangage state module description and check**mk** Agent Installation example states comming soon ...


