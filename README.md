# Honey-wall

Honey-wall is an HTTP and SSH-based low interaction honeypot.

## Prerequisites

Move the ssh to use port 2268

```bash
vi /etc/ssh/sshd_config
Change port to use 2268
sudo service ssh restart
```

## Run

```bash
chmod +x *.sh
sudo ./server.sh
```
