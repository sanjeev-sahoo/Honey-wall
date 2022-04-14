#!/bin/bash

iptables -A INPUT -s $1 -p tcp --destination-port 2268 -j DROP
