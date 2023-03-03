# az-demo-ansible

Demo CheckMK site in Azure with Ansible.

## Ansible check

Save `id_rsa` in the current working directory.

```console
$ ansible --private-key id_rsa -m ping all
demo.xantara-it.nl | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```

## Bootstrap Ansible

```console
$ ansible-playbook --user xantara --private-key id_rsa site.yml

PLAY [all] *************************************************************************************************************************

TASK [Gathering Facts] *************************************************************************************************************
ok: [demo.xantara-it.nl]

TASK [update/upgrade package cache] ************************************************************************************************
ok: [demo.xantara-it.nl]

...

TASK [cleanup package cache] *******************************************************************************************************
ok: [demo.xantara-it.nl]

PLAY RECAP *************************************************************************************************************************
demo.xantara-it.nl         : ok=18   changed=13   unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

```
