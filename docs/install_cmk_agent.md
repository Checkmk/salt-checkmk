# Install check**mk** Agent via Salt

| Todos |
|-------|
|Provide installation method for Unix (AIX, Solaris, ...) |
||

**Currently supported minion operating systems**
- Linux
- Windows


--- 

## Windows
Refresh package database on Windows Minions to publish the agent package from formula
```bash
salt -G 'os:windows' pkg.refresh_db
```
## Install check**mk** Agent on your Minions
```
salt \* state.apply cmk-manage.deploy-cmk-agent
```

**Sources**
* [Salt Windows Software Repository](https://docs.saltstack.com/en/latest/topics/windows/windows-package-manager.html)

Example output:

![Example](/docs/images/install_cmk_agent_example.png)

---
|**Previous**||||**Next**|
|:-|-|-|-|-:|
| <  [Pillar & Grains](cmk_pillar_grains.md)||^[Top](#install-check*mk*-Agent-via-Salt)|| [Add Salt Minions to check**mk**](add_minions_to_cmk.md)>| 
