## Getting Started

1. Log into your check**mk** environment

    In case that you have not already a running check**mk** environment, setup a new one e.g.:   
    https://hub.docker.com/r/checkmk/check-mk-raw
    
    ```bash
    docker container run -dit -p 8080:5000 -v /omd/sites --name monitoring -v /etc/localtime:/etc/localtime --restart always checkmk/check-mk-raw:1.6.0-latest
    
    #gather the logon credentials from container logs
    docker logs -f <id>
    ```
    Open your Browser and perform login to cmk container
    
     `http://localhost:8080/cmk`
    
    ![checkmk logon](/doc/images/cmk-logon.png)
    
    Click on the left sidebar on **WATO · Configuration** ->  "Users"
    
    Edit user `automation`:
    
    ![checkmk automation user](/doc/images/cmk-automation-user.png)
    
    Copy "Automation secret for machine accounts" (e.g. 7ffb0ff9-d907-4140-b95e-fb9d9df2a5)
    
2. Test the Salt check-mk-web-api Module

    ```bash
    salt-call check-mk-web-api.call method=get_all_users target=localhost site=cmk port=8080 user=automation secret=<paste here the automation secret>
    ```
