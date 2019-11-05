# Activate Minion Monitoring

Open your Browser and perform login to check**mk**

|          |                                     |
|----------|-------------------------------------|
| **URL**  |  http://`<IP MK Minion>`:8080/cmk   |
| **USER** |  cmkadmin                           |
| **PASSWORD** |  initial password (show docker logs) |
 

![checkmk logon](images/cmk-logon.png)

Click on the left sidebar on **WATO · Configuration** ->  "Hosts"

![wato-conf-hosts](images/wato_conf_hosts.png)

## Discover Monitoring Metrics (services)
Click on Bulk discovery
![wato-conf-hosts-discovery](images/wato_conf_hosts_bulk_discovery.png)

Start discovery with default settings
Click on Start ->

![start](images/wato_button_start.png)

Check**mk** will now discover automatically  monitoring metrics (e.g. Filesystems, Network Interfaces, CPU, Memory, ... )

![wato-conf-hosts-discovery-example](images/wato_conf_hosts_bulk_discovery_example.png)

After successful discovery click on Back

![back](images/wato_button_back.png)

## Activate Changes

Every configuration change in check**mk** (this includes changes by Salt and Web-API) will be tracked. Before the configuration will be effective you have to activate these changes.

The activation can be also done via Salt, but for a better understanding I like to demonstrated it in the Web Administration Tool (WATO)

![changes](images/wato_conf_changes.png)

![activate-changes](images/wato_conf_activate_changes.png)


## Monitor your Minions at glance

Open the Main Overview with a click on the "mk"

![open-main-overview](images/wato_open_main_overview.png)

### Dashboard Overview Example

![main-overview](images/wato_main_overview_example.png)



