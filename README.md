# Honey-wall

Honey-wall is an HTTP and SSH-based low interaction honeypot.

## Prerequisites

Move the ssh to use port 2268

```bash
vi /etc/ssh/sshd_config
Change port to use 2268
sudo service ssh restart
```

## Free the ports
```bash
chmod +x *.sh
sudo kill-script.sh
```

## Run

```bash
sudo ./server.sh
```
