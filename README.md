SPDX-FileCopyrightText: © 2021 Yake Ho Foong

SPDX-License-Identifier: BSD-3-Clause


# HadoopMahoutPseudoDistributedCluster
An Ansible playbook (script) to setup a pseudo-distributed cluster for testing Hadoop and Mahout projects.

## Background
Hadoop allows the setup of a pseudo-distributed operation (on 1 single PC) for testing, which is useful for testing out small projects when an actual cluster is not available. Interaction with the pseudo-distributed “cluster” should be just like an actual cluster, where instructions are sent from the Master Node. This repository was tested using a Windows Subsystem for Linux 2 (WSL2) using an Ubuntu 20.04 LTS image installed from the Microsoft Store. I believe it should work the same way if I had used an Ubuntu image on a virtual machine. WSL2 is used here for computing speed. WSL2 runs a full Linux kernel.

The reason for sharing this Ansible Playbook is that setting up Mahout is not straightforward, and information on the internet is mostly not easy to follow. The goal here is to have a single easy to use tool to setup the environment.

It is strongly recommended to run this on a PC with SDD rather than HDD, to ensure sufficient speed, as Hadoop's Map Reduce does not process calculations in-memory, but rather, on-disk.

I was unable to get the latest version of Mahout (0.14) to run on the latest version of Hadoop (3.3.1). After searching on the internet, I concluded that Mahout has phased out Map Reduce. The last version supporting Map Reduce was Mahout 0.9 (yar 2014) with support confirmed for Hadoop binaries 1.2.1. Some websites mentioned that Mahout 0.9 may be able to work with Hadoop releases above 1.2.1 e.g. 2 or even 3, but would need rebuilding from source with some adjustments. I tried rebuilding using Maven but failed. Hence, I have setup Mahout 0.9 with Hadoop 1.2.1, both from binaries, under a user login “mahout09”, and then setup Hadoop 3.3.1 only, also from binaries, under another user login “hadoop331”. The environment variables are setup to point to the separate versions, to keep them separate. Logging in as hadoop331 allows one to test using the latest Hadoop (3.3.1), while logging in as mahout09 allows one to test using Mahout.

The provisioning of this pseudo-distributed “cluster” is setup in an Ansible playbook. The reason for choosing Ansible is because Ansible playbooks have idempotency property, ensuring assurance of reproducibility.

## Setup Instructions
1.	From a fresh Ubuntu image, run “setup_ansible.sh”:  
$ chmod +x setup_ansible.sh  
$ bash setup_ansible.sh  
2.	Edit the attached file “vars.yml”. Replace the 2 “password_hash” item with your own values. You can get the hash value for your own chosen password by running:  
$ mkpasswd --method=sha-512  
You will be asked to key in your chosen password.  
3.	Then, run the following with the files “big_data.yml” with “vars.yml” in the same folder:  
$ sudo ansible-playbook big_data.yml  
Note that the playbook removes and purges the package openssh-server, and then installs it again. This is due to some issues in WSL2.  
4.	Switch to user mahout09:  
$ su - mahout09  
5.	Start the ssh service:  
$ sudo service ssh start  
6.	Run:  
$ ssh localhost  
Answer “yes” when you are asked “are you sure you want to continue?”.  
7.	Run the following to start the Hadoop service:  
$ start-all.sh  
8.	Run the following to prepare the Hadoop cluster:  
$ hadoop namenode -format  
$ hadoop fs -mkdir /user  
$ hadoop fs -mkdir /user/mahout09  
9.	Run the following to stop the Hadoop service before you log off this user:  
$ stop-all.sh  
10.	Repeat steps 5 to 9 for user “hadoop331”, except for Step 8, run:  
$ hdfs namenode -format  
$ hdfs dfs -mkdir /user  
$ hdfs dfs -mkdir /user/hadoop331  
After formatting run this to check  
$ hdfs dfs -ls /  

Note that when running Mahout 0.9 with Hadoop 1.2.1, the following warning message will keep appearing:  
localhost: WARNING: An illegal reflective access operation has occurred  
According to the website below, this is due to Hadoop 1.2.1 and can be safely ignored.  
https://stackoverflow.com/questions/52155078/how-to-fix-hadoop-warning-an-illegal-reflective-access-operation-has-occurred-e  

## Using the Pseudo Distributed Cluster
Upon logging on always run:  
$ start-all.sh  
And before logging off, always run:  
$ stop-all.sh  
Notice that for Hadoop 1.2.1, the file system commands are:  
$ hdfs dfs -linux_command   
$ hadoop fs -linux_command  
whereas for Hadoop 3.3.1, the commands are:  
$ hdfs dfs -linux_command  
