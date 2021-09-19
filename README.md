# [esxi_kms](https://github.com/sbhhbs/esxi_kms)

A Simple KMS(KIMP) for ESXi/vSphere. So you can add a TPM for Windows 11 😂. 

__⚠️DO NOT USE IN Production__

This server is based on [PyKIMP](https://github.com/OpenKMIP/PyKMIP) and saves data in a simple sqlite. 

It is modified to not validate client certificate. (Even less secure, but can be very easily set up in vSphere)

## How to use

Docker compose:
```
version: '2'
services:
  kms:
    image: sbhhbs/esxi_kms
    volumes:
    - /volume/on/host/config:/root/app/config/:ro
    - /volume/on/host/storage:/root/app/storage
    ports:
    - 5696:5696/tcp
```

Basically, the image expect a `config` directory and a `storage` directory in `/root/app`

`config` should contains a `server.conf` (for what can be put there, see [PyKMIP's doc](https://pykmip.readthedocs.io/en/latest/server.html#configuration)). 

`storage` directory is where the sqlite saved data will be.

`config` in git contains example config and certificates. You can use it as is (and it is of course not secure)or generate new certificate by running `python gen_certs.py`
