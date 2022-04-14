#!/bin/bash -e

function cleanup {
  echo "Removing /tmp/foo"
  rm  -rf abcd.py
  rm  -rf touch 
}

trap cleanup EXIT
mkdir touch
touch abcd.py
chmod +x abcd.py
asdffdsa #Fails
