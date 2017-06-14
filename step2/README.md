#### Name: step2
#### Run: ./run\_ansible [any allowed argument to ansible-playbook]


### Description: 
Edit variables inside playbook.yml `vars:` section to adjust behvior.

```yaml
vars:
  action_type: manage | list
  state: present | absent
  username: user_name_here
  pubkey: "ssh-rsa AAAAB3NzaC1y...."
```


### Override:
any var in playbook may be override from command line with `./run\_ansible -e action\_type=list`
