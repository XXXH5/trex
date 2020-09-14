#!/bin/bash
#for ((loop = 2; loop <= 36; loop++))
#do
# ping "192.168.1."$loop -c 1
#done
#echo 
cd /root/v2.75
device=`route -n|grep 192.168 |awk '{print $8}'`
#device=`ip a|grep 192.168 |awk '{print $9}'`
nic=`echo $device |awk '{print $1}'`
pci_ids=`./dpdk_setup_ports.py -s | grep 0000 | grep -v $nic | awk '{print $1}' | awk -F 0000: '{print $2}'`
echo $pci_ids
pci_id_1=`echo $pci_ids |awk '{print $1}'`
pci_id_2=`echo $pci_ids |awk '{print $2}'`
echo $pci_id_1,$pci_id_2
#sed -i "s/\"..\:..\..\"\,\"..\:..\..\"/\"$pci_id_1\",\"$pci_id_2\"/g" /etc/trex_cfg.yaml
sed -i "4c \  interfaces    : [\"$pci_id_1\",\"$pci_id_2\"]" /etc/trex_cfg.yaml 
./trex_daemon_server start

