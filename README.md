# az-demo-ansible

Demo CheckMK site in Azure with Ansible.

## Ansible check

```console
$ ansible --private-key ../az-demo-terraform/id_rsa -m ping all
demo.xantara-it.nl | SUCCESS => {
    "changed": false,
    "ping": "pong"
}
```
