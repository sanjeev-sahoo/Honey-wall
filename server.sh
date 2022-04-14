#!/bin/bash -e

function cleanup {
  rm  -rf abcd.py
  rm  -rf touch
}
#sudo su
trap cleanup EXIT
#sudo python ssh.py
sudo python3 webserver.py & sudo python ssh.py
