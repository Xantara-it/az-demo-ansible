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

