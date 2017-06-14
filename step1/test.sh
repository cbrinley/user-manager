#!/bin/bash

test `uname` == "Linux" || { echo "This test only works on linux"; exit 1; }

PUB_KEY=/home/vagrant/.ssh/id_rsa.pub
test -f $PUB_KEY || { echo $PUB_KEY is not valid. set to valid key; exit 1; }
SSH_KEY=`cat $PUB_KEY`

./user-manager add test-user -m || { echo fail add user; exit 1; }
./user-manager ls | grep test-user &>/dev/null || { echo fail ls user; exit 1; }
./user-manager ssh test-user "$SSH_KEY" || { echo fail add ssh key; exit 1; }

#test ssh access
if [ -z "$SUDO_USER" ]; then
  ssh test-user@localhost "hostname" &>/dev/null || { echo fail ssh login; exit 1; }
else
  sudo -u $SUDO_USER ssh test-user@localhost "hostname" &>/dev/null || { echo fail ssh login; exit 1; }
fi

#clean up
./user-manager rm -r test-user || { echo fail rm  user; exit 1; }