# SPDX-FileCopyrightText: © 2021 Yake Ho Foong
# SPDX-License-Identifier: BSD-3-Clause

#!/bin/bash

sudo apt update
sudo apt upgrade
sudo apt-get install -y python3-pip python3-dev
sudo pip3 install lxml
sudo pip3 install ansible
ansible-galaxy collection install community.general
sudo apt-get install -y whois
