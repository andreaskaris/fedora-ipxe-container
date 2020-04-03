#!/bin/bash

# render /tftpboot/menu/boot.ipxe
./render_boot_ipxe.py
mv boot.ipxe /tftpboot/menu/boot.ipxe

# render /etc/dnsmasq.conf
./render_config.py
mv dnsmasq.conf /etc/dnsmasq.conf

# run dnsmasq
/usr/sbin/dnsmasq -k --log-facility=/dev/stdout &

# sleep for all eternity
sleep infinity
