#!/bin/bash

# render /tftpboot/menu/boot.ipxe
# adds inotify hooks to the directory 
# so that live changes are reflected in
# /tftpboot/menu/boot.ipxe
./render_boot_ipxe.py &

# render /etc/dnsmasq.conf
./render_config.py
mv dnsmasq.conf /etc/dnsmasq.conf

# run dnsmasq
/usr/sbin/dnsmasq -k --log-facility=/dev/stdout &

# run httpd
# making my life easier - just link this instead of reconfiguring httpd
# needs to be unlink as on container restart this would be a link not a dir
unlink /var/www/html
ln -s /httpboot /var/www/html
/usr/sbin/httpd -DFOREGROUND &

# sleep for all eternity
sleep infinity
