# Add Salt Minions to check**mk**

## Add Minions

  ```bash
  salt <MK Minion> state.apply cmk-manage.add-minions
  ```

By default the state will add your Minions to check**mk** with the following data set.

| Checkmk value |Salt Grain(s) |
|---------------|--------------|
| Hostname      | id           |
| Alias         | host         |
| Ipv4 Address  | ipv4[0]  | 
| Host-Tags     | All Grains defined in Graintags |

If your Minion has multiple ip addresses you can assign the monitoring ip address with the custom grain *cmk-agent-ip*. 

Example:
vi /etc/salt/grains

```yaml
cmk-agent-ip: 192.168.56.27
```
```bash
systemctl restart salt-minion.service
```

|**Previous**|[Top](#add-salt-minions-to-check**mk**)|**Next**|
|:-|-|-:|
| < [Install check**mk** Agent via Salt](install_cmk_agent.md) || [Activate Minion Monitoring](activate_minion_monitoring.md) >| 
