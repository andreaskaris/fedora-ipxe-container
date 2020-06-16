#!/bin/bash

echo "Installing Fedora PXE boot image for debugging"
curl -L -o /tmp/fedora.iso "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Server/x86_64/iso/Fedora-Server-dvd-x86_64-32-1.6.iso"
mkdir /mnt/fedora
mkdir /httpboot/fedora/dvd -p
mount -o loop /tmp/fedora.iso /mnt/fedora
\cp -a /mnt/fedora/* /httpboot/fedora/dvd/.
\cp /httpboot/fedora/dvd/images/pxeboot/* /httpboot/fedora/.
umount /mnt/fedora
cat << 'EOF' > /httpboot/fedora/boot-menu-entry 
set server_root http://{{ PXE_LISTEN_ADDRESS }}:{{ PXE_LISTEN_PORT }}/fedora/
initrd ${server_root}/initrd.img
kernel ${server_root}/vmlinuz ip=dhcp ipv6.disable initrd=initrd.img inst.ks=${server_root}/kickstart.cfg
boot
EOF
source config 
cat << EOF > /httpboot/fedora/kickstart.cfg
url --url http://${PXE_LISTEN_ADDRESS}:${PXE_LISTEN_PORT}/fedora/dvd/
timezone --utc America/New_York
lang en_US.UTF-8
keyboard us
rootpw --plaintext password
reboot
firstboot --disable
services --enabled="sshd,chronyd"
zerombr
clearpart --all
autopart --type lvm
%packages
@core
%end
EOF
