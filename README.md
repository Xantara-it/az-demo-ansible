# az-demo-ansible

Demo CheckMK site in Azure with Ansible.

## Ansible check

Save `id_rsa` in the current working directory.

```console
$ ansible -m ping all
demo.xantara-it.nl | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
