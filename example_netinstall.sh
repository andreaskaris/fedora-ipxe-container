#!/bin/bash

echo "Installing Fedora PXE boot image for debugging"
curl -L -o /tmp/fedora.iso "https://download.fedoraproject.org/pub/fedora/linux/releases/32/Server/x86_64/iso/Fedora-Server-netinst-x86_64-32-1.6.iso"
mkdir /mnt/fedora
mount -o loop /tmp/fedora.iso /mnt/fedora/
mkdir /httpboot/fedora
\cp /mnt/fedora/images/pxeboot/* /httpboot/fedora/.
umount /mnt/fedora
cat << 'EOF' > /httpboot/fedora/boot-menu-entry 
set server_root http://{{ PXE_LISTEN_ADDRESS }}/fedora/
initrd ${server_root}/initrd.img
kernel ${server_root}/vmlinuz ip=dhcp ipv6.disable initrd=initrd.img inst.ks=${server_root}/kickstart.cfg
boot
EOF
cat << 'EOF' > /httpboot/fedora/kickstart.cfg
network --bootproto=dhcp --device=bootif
rootpw --plaintext password
reboot
repo --name=fedora
repo --name=updates
firstboot --disable
services --enabled="sshd,chronyd"
zerombr
clearpart --all
autopart --type lvm
%packages
@core
%end
EOF
