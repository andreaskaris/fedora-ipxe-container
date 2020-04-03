#!/bin/bash

# render /tftpboot/menu/boot.ipxe
./render_boot_ipxe.py
mv boot.ipxe /tftpboot/menu/boot.ipxe

# render /etc/dnsmasq.conf
./render_config.py
mv dnsmasq.conf /etc/dnsmasq.conf

# run dnsmasq
/usr/sbin/dnsmasq -k --log-facility=/dev/stdout &

# run httpd
# making my life easier - just link this instead of reconfiguring httpd
rmdir /var/www/html
ln -s /httpboot /var/www/html
/usr/sbin/httpd -DFOREGROUND &

# sleep for all eternity
sleep infinity
