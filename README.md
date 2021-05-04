# Combine Checkmk & Salt

![checkmk_salt](/docs/images/checkmk_salt.png)

## General Information
This project describes how you can combine the powerful solutions **checkmk** (monitoring) & **Salt** (data center automation)


The project was initially created for the checkmk conference #5 /2019. In the meanwhile there are a lot of changes done in the back-end and APIs of checkmk and also in salt (both solutions switched to Pyhton3). Therefore I like to share much more simplified content, instead of the special use cases from the conference. The new stuff should be applicable and compatible to the current versions of Checkmk & Salt.

## Environment Scope
- Define & Create
- Configure 
- Update 

The State is designed to carry out changes only if they are necessary to define the specified check mk omd environment.  


### Define & create Checkmk environments
![create-sites](/docs/videos/create-sites.gif)  

### Configure and modify environments
![modify-sites](/docs/videos/modify-sites.gif)  

### Update environments
![update-sites](/docs/videos/update-sites.gif)  

## Quickstart
To test the setup on a single host
```bash
sudo git clone https://github.com/tribe29/salt-checkmk.git /srv/formulas/salt-checkmk

# install salt minion
curl -fsSL https://bootstrap.saltproject.io -o install_salt.sh
sudo sh install_salt.sh -P -x python3

# apply salt masterless config
/srv/formulas/salt-checkmk/files/apply_masterless.sh

# define / configure your omd environment
vi /srv/pillar/omd.sls

# create your environment
# please ensure that the defined omd packages are installed on system (can easily done via salt, but currently out of scope) 
salt-call --local state.apply omd
```


